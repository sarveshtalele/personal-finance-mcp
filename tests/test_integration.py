"""
Integration Tests — verify the MCP tool layer works end-to-end.

These tests call the tool functions (which internally call calculators)
and verify the full pipeline: input → calculator → formatter → string output.
"""

# ---------------------------------------------------------------------------
# Helper: import the register function and build a mini-MCP for each module
# ---------------------------------------------------------------------------
from src.server import mcp


class TestServerRegistration:
    """Verify all tool modules register correctly on the MCP server."""

    def test_total_tool_count(self):
        tools = mcp._tool_manager._tools
        assert len(tools) == 77, f"Expected 77 tools, got {len(tools)}"

    def test_tvm_tools_present(self):
        tool_names = list(mcp._tool_manager._tools.keys())
        expected = [
            "calculate_future_value",
            "calculate_present_value",
            "calculate_annuity_fv",
            "calculate_annuity_pv",
            "calculate_perpetuity",
            "calculate_rule_of_72",
            "calculate_effective_rate",
            "calculate_real_return",
            "calculate_inflation_impact",
            "calculate_savings_needed",
        ]
        for name in expected:
            assert name in tool_names, f"Missing TVM tool: {name}"

    def test_debt_tools_present(self):
        tool_names = list(mcp._tool_manager._tools.keys())
        expected = [
            "calculate_emi",
            "loan_amortization",
            "compare_loans",
            "calculate_prepayment_savings",
            "invest_or_prepay_loan",
            "analyze_debt_consolidation",
        ]
        for name in expected:
            assert name in tool_names, f"Missing debt tool: {name}"

    def test_planning_tools_present(self):
        tool_names = list(mcp._tool_manager._tools.keys())
        expected = [
            "calculate_net_worth",
            "analyze_financial_ratios",
            "calculate_emergency_fund",
            "analyze_budget",
            "plan_financial_goal",
            "plan_retirement",
            "plan_education",
            "calculate_insurance_need",
            "financial_health_check",
        ]
        for name in expected:
            assert name in tool_names, f"Missing planning tool: {name}"

    def test_bond_tools_present(self):
        tool_names = list(mcp._tool_manager._tools.keys())
        expected = [
            "calculate_bond_price",
            "calculate_ytm",
            "calculate_current_yield",
            "calculate_bond_duration",
            "calculate_bond_convexity",
            "calculate_zero_coupon_bond",
        ]
        for name in expected:
            assert name in tool_names, f"Missing bond tool: {name}"

    def test_stock_tools_present(self):
        tool_names = list(mcp._tool_manager._tools.keys())
        expected = [
            "value_stock_ddm",
            "value_stock_two_stage_ddm",
            "value_stock_pe",
            "value_stock_dcf",
            "calculate_dividend_yield",
        ]
        for name in expected:
            assert name in tool_names, f"Missing stock tool: {name}"

    def test_mf_tools_present(self):
        tool_names = list(mcp._tool_manager._tools.keys())
        expected = [
            "calculate_sip_returns",
            "calculate_sip_needed",
            "compare_lumpsum_vs_sip",
            "analyze_expense_ratio_impact",
            "calculate_swp",
            "calculate_cagr",
            "calculate_nav",
        ]
        for name in expected:
            assert name in tool_names, f"Missing MF tool: {name}"

    def test_portfolio_tools_present(self):
        tool_names = list(mcp._tool_manager._tools.keys())
        expected = [
            "calculate_portfolio_return",
            "calculate_portfolio_risk",
            "analyze_two_asset_portfolio",
            "calculate_capm_return",
            "calculate_sharpe_ratio",
            "calculate_treynor_ratio",
            "calculate_jensens_alpha",
            "calculate_information_ratio",
            "calculate_sortino_ratio",
            "suggest_asset_allocation",
            "rebalance_portfolio",
        ]
        for name in expected:
            assert name in tool_names, f"Missing portfolio tool: {name}"


class TestToolOutputFormat:
    """Verify that tool outputs follow the expected format conventions."""

    def test_fv_output_has_reference(self):
        from src.tools.tvm import register as tvm_register
        from mcp.server.fastmcp import FastMCP

        test_mcp = FastMCP("test")
        tvm_register(test_mcp)

        # Get the tool function directly
        tool_fn = test_mcp._tool_manager._tools["calculate_future_value"].fn
        output = tool_fn(100000, 12, 10, "monthly")
        assert "Future Value" in output
        assert "₹" in output

    def test_emi_output_has_formula(self):
        from src.tools.debt import register as debt_register
        from mcp.server.fastmcp import FastMCP

        test_mcp = FastMCP("test")
        debt_register(test_mcp)

        tool_fn = test_mcp._tool_manager._tools["calculate_emi"].fn
        output = tool_fn(5000000, 8.5, 20)
        assert "EMI" in output
        assert "₹" in output
        assert "Formula" in output

    def test_bond_output_has_sections(self):
        from src.tools.bonds import register as bond_register
        from mcp.server.fastmcp import FastMCP

        test_mcp = FastMCP("test")
        bond_register(test_mcp)

        tool_fn = test_mcp._tool_manager._tools["calculate_bond_price"].fn
        output = tool_fn(1000, 8, 10, 5, 2)
        assert "Bond" in output

    def test_planning_output_has_sections(self):
        from src.tools.planning import register as planning_register
        from mcp.server.fastmcp import FastMCP

        test_mcp = FastMCP("test")
        planning_register(test_mcp)

        tool_fn = test_mcp._tool_manager._tools["plan_financial_goal"].fn
        output = tool_fn("Buy House", 5000000, 10, 6, 12, 500000)
        assert "Buy House" in output
        assert "SIP" in output
        assert "₹" in output


class TestEndToEndScenarios:
    """
    End-to-end test scenarios that simulate real-world Claude Desktop usage.
    Each test calls multiple tools in sequence — the way a real user would.
    """

    def test_retirement_planning_flow(self):
        """Simulate: 'I'm 30, earn 1.5L/month — plan my retirement.'"""
        from src.tools.tvm import inflation_adjusted_amount, required_monthly_savings

        # Step 1: Inflate current expenses to retirement age
        inflated = inflation_adjusted_amount(60000, 6, 30)
        assert inflated["future_amount"] > 60000
        assert inflated["inflation_multiplier"] > 1

        # Step 2: Calculate corpus needed (simplified)
        monthly_need = inflated["future_amount"]
        real_rate = (1 + 0.08) / (1 + 0.06) - 1
        if real_rate > 0:
            r = real_rate / 12
            n = 25 * 12  # 25 year retirement
            corpus = monthly_need * ((1 - (1 + r) ** (-n)) / r)
        else:
            corpus = monthly_need * 12 * 25
        assert corpus > 0

        # Step 3: Monthly SIP needed
        savings = required_monthly_savings(corpus, 12, 30, 0)
        assert savings["monthly_savings_needed"] > 0

    def test_debt_analysis_flow(self):
        """Simulate: 'Should I prepay my home loan or invest in MF?'"""
        from src.tools.debt import calculate_emi, invest_vs_prepay

        # Step 1: Current loan
        emi = calculate_emi(5000000, 8.5, 20)
        assert emi["emi"] == 43391.16

        # Step 2: Investment vs prepayment decision
        decision = invest_vs_prepay(8.5, 15, 30, True)
        assert "recommendation" in decision
        assert decision["net_benefit_of_investing"] > 0  # 15% return >> 8.5% loan

    def test_sip_and_goal_planning_flow(self):
        """Simulate: 'I need 1 crore in 15 years, how much SIP?'"""
        from src.tools.mutual_funds import sip_required_for_target
        from src.tools.tvm import inflation_adjusted_amount

        # Step 1: Adjust for inflation
        inflated = inflation_adjusted_amount(10000000, 6, 15)  # 1 Cr today
        target = inflated["future_amount"]
        assert target > 10000000

        # Step 2: SIP needed
        sip = sip_required_for_target(target, 12, 15)
        assert sip["monthly_sip_needed"] > 0
        assert sip["total_invested"] < target  # proves compounding works

    def test_stock_bond_portfolio_flow(self):
        """Simulate: 'Value this stock and create a 60/40 portfolio.'"""
        from src.tools.stocks import gordon_growth_model
        from src.tools.bonds import bond_price
        from src.tools.portfolio import portfolio_expected_return, sharpe_ratio

        # Step 1: Value a stock
        stock = gordon_growth_model(10, 8, 15)
        assert "intrinsic_value" in stock
        assert stock["intrinsic_value"] > 0

        # Step 2: Price a bond
        bond = bond_price(1000, 8, 10, 5, 2)
        assert "bond_price" in bond

        # Step 3: Portfolio
        port_ret = portfolio_expected_return([0.6, 0.4], [15, 8])
        assert port_ret["portfolio_expected_return"] == 12.2

        # Step 4: Risk-adjusted return
        sr = sharpe_ratio(12.2, 6, 10)
        assert sr["sharpe_ratio"] > 0
