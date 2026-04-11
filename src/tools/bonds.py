"""
Bond Pricing and Yield Calculations

Core formulas:
  Bond Price = Σ [C/(1+r)^t] + FV/(1+r)^n
  Current Yield = Annual Coupon / Market Price
  YTM: Price = Σ [C/(1+y)^t] + FV/(1+y)^n  (solved iteratively)
  Macaulay Duration = Σ [t × PV(CF_t)] / Bond Price
  Modified Duration = Macaulay Duration / (1 + y/n)
  Convexity = Σ [t(t+1) × PV(CF_t)] / (Price × (1+y)^2)
"""


def bond_price(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
) -> dict:
    """
    Calculate bond price using DCF.
    Price = Σ [C/(1+r)^t] + FV/(1+r)^n
    """
    c = face_value * (coupon_rate / 100) / coupon_frequency
    r = ytm / 100 / coupon_frequency
    n = int(years_to_maturity * coupon_frequency)

    if r == 0:
        pv_coupons = c * n
        pv_face = face_value
    else:
        pv_coupons = c * (1 - (1 + r) ** (-n)) / r
        pv_face = face_value / (1 + r) ** n

    price = pv_coupons + pv_face

    if price > face_value:
        premium_discount = "Premium (Price > Face Value)"
    elif price < face_value:
        premium_discount = "Discount (Price < Face Value)"
    else:
        premium_discount = "At Par"

    return {
        "bond_price": round(price, 2),
        "pv_of_coupons": round(pv_coupons, 2),
        "pv_of_face_value": round(pv_face, 2),
        "coupon_per_period": round(c, 2),
        "total_periods": n,
        "premium_or_discount": premium_discount,
        "premium_discount_amount": round(price - face_value, 2),
        "formula": f"Price = Σ[{c:.2f}/(1+{r:.4f})^t] + {face_value}/(1+{r:.4f})^{n}",
    }


def current_yield(annual_coupon: float, market_price: float) -> dict:
    """Current Yield = Annual Coupon / Market Price"""
    cy = (annual_coupon / market_price) * 100

    return {
        "current_yield": round(cy, 4),
        "annual_coupon": annual_coupon,
        "market_price": market_price,
        "formula": f"CY = {annual_coupon} / {market_price} × 100 = {cy:.4f}%",
    }


def yield_to_maturity(
    face_value: float,
    coupon_rate: float,
    market_price: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
) -> dict:
    """
    Calculate YTM using iterative Newton-Raphson method.
    Solve: Price = Σ [C/(1+y)^t] + FV/(1+y)^n for y
    """
    c = face_value * (coupon_rate / 100) / coupon_frequency
    n = int(years_to_maturity * coupon_frequency)

    # Approximate YTM using formula:
    # YTM ≈ [C + (FV - P)/n] / [(FV + P)/2]
    annual_coupon = face_value * coupon_rate / 100
    approx_ytm = (annual_coupon + (face_value - market_price) / years_to_maturity) / (
        (face_value + market_price) / 2
    )

    # Newton-Raphson refinement
    ytm_guess = approx_ytm / coupon_frequency

    for _ in range(200):
        price = 0
        dprice = 0
        for t in range(1, n + 1):
            df = (1 + ytm_guess) ** t
            price += c / df
            dprice -= t * c / (df * (1 + ytm_guess))
        price += face_value / (1 + ytm_guess) ** n
        dprice -= n * face_value / ((1 + ytm_guess) ** n * (1 + ytm_guess))

        diff = price - market_price
        if abs(diff) < 0.0001:
            break
        ytm_guess -= diff / dprice

    ytm_annual = ytm_guess * coupon_frequency * 100

    return {
        "ytm": round(ytm_annual, 4),
        "ytm_per_period": round(ytm_guess * 100, 4),
        "approximate_ytm": round(approx_ytm * 100, 4),
        "market_price": market_price,
        "face_value": face_value,
        "coupon_rate": coupon_rate,
        "formula": "YTM ≈ [C + (FV - P)/n] / [(FV + P)/2]",
    }


def bond_duration(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
) -> dict:
    """
    Calculate Macaulay Duration and Modified Duration.
    Macaulay: D = Σ [t × PV(CF_t)] / Price
    Modified: D_mod = D_mac / (1 + y/n)
    """
    c = face_value * (coupon_rate / 100) / coupon_frequency
    r = ytm / 100 / coupon_frequency
    n = int(years_to_maturity * coupon_frequency)

    price = 0
    weighted_pv = 0

    for t in range(1, n + 1):
        cf = c if t < n else c + face_value
        pv = cf / (1 + r) ** t
        price += pv
        weighted_pv += t * pv

    macaulay_duration = weighted_pv / price  # in periods
    macaulay_years = macaulay_duration / coupon_frequency
    modified_duration = macaulay_years / (1 + r)

    # Price sensitivity
    price_change_1pct = -modified_duration * 1  # % change for 1% rate increase

    return {
        "macaulay_duration_periods": round(macaulay_duration, 4),
        "macaulay_duration_years": round(macaulay_years, 4),
        "modified_duration": round(modified_duration, 4),
        "bond_price": round(price, 2),
        "price_change_for_1pct_rate_rise": round(price_change_1pct, 4),
        "interpretation": f"For every 1% increase in yield, bond price drops approximately {abs(price_change_1pct):.2f}%",
        "formula": "D_mac = Σ[t × PV(CF_t)] / Price; D_mod = D_mac / (1 + y/n)",
    }


def bond_convexity(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    years_to_maturity: float,
    coupon_frequency: int = 2,
) -> dict:
    """
    Calculate bond convexity.
    Convexity = Σ [t(t+1) × PV(CF_t)] / [Price × (1+y)^2]
    """
    c = face_value * (coupon_rate / 100) / coupon_frequency
    r = ytm / 100 / coupon_frequency
    n = int(years_to_maturity * coupon_frequency)

    price = 0
    convexity_sum = 0

    for t in range(1, n + 1):
        cf = c if t < n else c + face_value
        pv = cf / (1 + r) ** t
        price += pv
        convexity_sum += t * (t + 1) * pv

    convexity = convexity_sum / (price * (1 + r) ** 2)
    convexity_years = convexity / (coupon_frequency**2)

    return {
        "convexity_periods": round(convexity, 4),
        "convexity_years": round(convexity_years, 4),
        "bond_price": round(price, 2),
        "interpretation": f"Higher convexity ({convexity_years:.2f}) means the bond price is less sensitive to large yield changes",
        "formula": "Convexity = Σ[t(t+1) × PV(CF_t)] / [Price × (1+y)²]",
    }


def zero_coupon_bond_price(
    face_value: float, ytm: float, years_to_maturity: float
) -> dict:
    """Price of zero-coupon bond = FV / (1+r)^n"""
    r = ytm / 100
    price = face_value / (1 + r) ** years_to_maturity
    discount = face_value - price

    return {
        "price": round(price, 2),
        "face_value": face_value,
        "discount": round(discount, 2),
        "ytm": ytm,
        "years_to_maturity": years_to_maturity,
        "formula": f"Price = {face_value} / (1 + {r})^{years_to_maturity}",
    }


from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="calculate_bond_price")
    def calculate_bond_price_tool(
        face_value: float,
        coupon_rate: float,
        ytm: float,
        years_to_maturity: float,
        coupon_frequency: int = 2,
    ) -> str:
        """Calculate bond price using DCF of coupon payments and face value.
        Price = Σ[C/(1+r)^t] + FV/(1+r)^n.
        coupon_frequency: 1=annual, 2=semi-annual, 4=quarterly."""
        result = bond_price(
            face_value, coupon_rate, ytm, years_to_maturity, coupon_frequency
        )
        return format_tool_response("Bond Pricing", result)

    @mcp.tool(name="calculate_ytm")
    def calculate_ytm_tool(
        face_value: float,
        coupon_rate: float,
        market_price: float,
        years_to_maturity: float,
        coupon_frequency: int = 2,
    ) -> str:
        """Calculate Yield to Maturity — the internal rate of return of a bond.
        Uses Newton-Raphson iteration for precision."""
        result = yield_to_maturity(
            face_value, coupon_rate, market_price, years_to_maturity, coupon_frequency
        )
        return format_tool_response("Yield to Maturity (YTM)", result)

    @mcp.tool(name="calculate_current_yield")
    def calculate_current_yield_tool(
        annual_coupon: float,
        market_price: float,
    ) -> str:
        """Calculate Current Yield = Annual Coupon / Market Price × 100."""
        result = current_yield(annual_coupon, market_price)
        return format_tool_response("Current Yield", result)

    @mcp.tool(name="calculate_bond_duration")
    def calculate_bond_duration_tool(
        face_value: float,
        coupon_rate: float,
        ytm: float,
        years_to_maturity: float,
        coupon_frequency: int = 2,
    ) -> str:
        """Calculate Macaulay Duration and Modified Duration.
        Duration measures interest rate sensitivity of a bond.
        Modified Duration shows % price change per 1% yield change."""
        result = bond_duration(
            face_value, coupon_rate, ytm, years_to_maturity, coupon_frequency
        )
        return format_tool_response("Bond Duration Analysis", result)

    @mcp.tool(name="calculate_bond_convexity")
    def calculate_bond_convexity_tool(
        face_value: float,
        coupon_rate: float,
        ytm: float,
        years_to_maturity: float,
        coupon_frequency: int = 2,
    ) -> str:
        """Calculate bond convexity — second-order measure of interest rate risk.
        Higher convexity = less price sensitivity to large yield changes."""
        result = bond_convexity(
            face_value, coupon_rate, ytm, years_to_maturity, coupon_frequency
        )
        return format_tool_response("Bond Convexity", result)

    @mcp.tool(name="calculate_zero_coupon_bond")
    def calculate_zero_coupon_bond_tool(
        face_value: float,
        ytm: float,
        years_to_maturity: float,
    ) -> str:
        """Price a zero-coupon bond. Price = FV / (1+r)^n.
        Zero-coupon bonds pay no periodic interest, sold at discount."""
        result = zero_coupon_bond_price(face_value, ytm, years_to_maturity)
        return format_tool_response("Zero Coupon Bond Pricing", result)
