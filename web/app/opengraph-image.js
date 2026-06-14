import { ImageResponse } from "next/og";

export const alt = "FinPlan MCP — financial planning tools for your AI";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OG() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: "80px",
          background: "linear-gradient(135deg, #06302c 0%, #0d9488 60%, #2dd4bf 100%)",
          color: "#fff",
          fontFamily: "sans-serif",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 28 }}>
          <div
            style={{
              width: 84,
              height: 84,
              borderRadius: 22,
              background: "rgba(255,255,255,0.15)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 52,
              fontWeight: 700,
            }}
          >
            ₹
          </div>
          <div style={{ fontSize: 34, fontWeight: 600, opacity: 0.92 }}>FinPlan MCP</div>
        </div>
        <div style={{ fontSize: 68, fontWeight: 800, lineHeight: 1.05, letterSpacing: -2, display: "flex" }}>
          Financial planning,
        </div>
        <div style={{ fontSize: 68, fontWeight: 800, lineHeight: 1.05, letterSpacing: -2, color: "#99f6e4", display: "flex" }}>
          answered by math.
        </div>
        <div style={{ fontSize: 30, marginTop: 30, opacity: 0.9, display: "flex" }}>
          77 deterministic finance tools · one MCP connector · live data
        </div>
      </div>
    ),
    { ...size }
  );
}
