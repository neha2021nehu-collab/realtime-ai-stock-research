import {useState, useEffect} from "react";
import axios from "axios";
import {BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid, Legend} from "recharts";

const API = "http://localhost:8000";

function SentimentBadge({ sentiment }) {
  const colors = {
    positive: "#22c55e",
    negative: "#ef4444",
    neutral:  "#f59e0b"
  };
  return (
    <span style ={{
      backgroundColor : colors[sentiment] || "#888",
      color : "white",
      padding : "2px 10px",
      borderRadius : "999px",
      fontSizez : "12px",
      fontWeight : 600
    }}>{sentiment}
    </span>
  );
}

export default function App() {
  const [headlines, setHeadlines] = useState([]);
  const [summary, setSummary]     = useState([]);
  const [trend, setTrend]         = useState([]);
  const [search, setSearch]       = useState("");
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    fetchAll();
  }, []);


  async function fetchAll() {
    setLoading(true);
    try{
      const [h, s, t] = await Promise.all([
        axios.get(`${API}/headlines?limit=50`),
        axios.get(`${API}/sentiment/summary`),
        axios.get(`${API}/sentiment/trend`)
      ]);
      setHeadlines(h.data.data);
      setSummary(s.data.data);
      setTrend(t.data.data.reverse().map(d => ({
        ...d,
        bucket : new Date(d.bucket).toLocaleTimeString([], {hour : "2-digit", minute: "2-digit"}),
        avg_score : parseFloat(d.avg_score.toFixed(3))
      })));
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  }

  async function handleSearch(e) {
    e.preventDefault();
    if (!search.trim()) return fetchAll();
    const res = await axios.get(`${API}/headlines/search?q=${search}`);
    setHeadlines(res.data.data);
  }

  if (loading) return (
    <div style={{ display: "flex", justifyContent: "center", alignItems:"center", height:"100vh", background:"#0f172a", color:"white", fontSize:"200px"}}>
      Loading Pipeline data...
    </div>
  );

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", color: "#e2e8f0", fontFamily: "system-ui, sans-serif", padding: "24px" }}>
      
      {/* Header */}
      <div style={{ marginBottom: "32px" }}>
        <h1 style={{ fontSize: "28px", fontWeight: 700, color: "#f8fafc", margin: 0 }}>
          📈 Real-Time Stock Sentiment
        </h1>
        <p style={{ color: "#94a3b8", marginTop: "4px" }}>Live financial news pipeline · Powered by Kafka + VADER + TimescaleDB</p>
      </div>

      {/* Summary Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px", marginBottom: "32px" }}>
        {summary.map(s => (
          <div key={s.sentiment} style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
            <p style={{ color: "#94a3b8", margin: 0, fontSize: "14px", textTransform: "capitalize" }}>{s.sentiment}</p>
            <p style={{ fontSize: "36px", fontWeight: 700, margin: "4px 0", color: s.sentiment === "positive" ? "#22c55e" : s.sentiment === "negative" ? "#ef4444" : "#f59e0b" }}>
              {s.count}
            </p>
            <p style={{ color: "#64748b", margin: 0, fontSize: "13px" }}>headlines</p>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "32px" }}>
        
        {/* Sentiment Distribution Bar Chart */}
        <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
          <h2 style={{ fontSize: "16px", marginTop: 0, color: "#f1f5f9" }}>Sentiment Distribution</h2>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={summary}>
              <XAxis dataKey="sentiment" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip contentStyle={{ background: "#0f172a", border: "none" }} />
              <Bar dataKey="count" fill="#6366f1" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Sentiment Trend Line Chart */}
        <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
          <h2 style={{ fontSize: "16px", marginTop: 0, color: "#f1f5f9" }}>Sentiment Trend (24h)</h2>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={trend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="bucket" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" domain={[-1, 1]} />
              <Tooltip contentStyle={{ background: "#0f172a", border: "none" }} />
              <Legend />
              <Line type="monotone" dataKey="avg_score" stroke="#6366f1" dot={false} strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

      </div>

      {/* Search + Headlines Table */}
      <div style={{ background: "#1e293b", borderRadius: "12px", padding: "20px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
          <h2 style={{ fontSize: "16px", margin: 0, color: "#f1f5f9" }}>Latest Headlines</h2>
          <form onSubmit={handleSearch} style={{ display: "flex", gap: "8px" }}>
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search headlines..."
              style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: "8px", padding: "8px 12px", color: "#e2e8f0", outline: "none", width: "220px" }}
            />
            <button type="submit" style={{ background: "#6366f1", color: "white", border: "none", borderRadius: "8px", padding: "8px 16px", cursor: "pointer" }}>
              Search
            </button>
            <button type="button" onClick={fetchAll} style={{ background: "#334155", color: "white", border: "none", borderRadius: "8px", padding: "8px 16px", cursor: "pointer" }}>
              Refresh
            </button>
          </form>
        </div>

        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid #334155", color: "#64748b", fontSize: "13px" }}>
              <th style={{ textAlign: "left", padding: "8px" }}>Headline</th>
              <th style={{ textAlign: "center", padding: "8px" }}>Sentiment</th>
              <th style={{ textAlign: "right", padding: "8px" }}>Score</th>
              <th style={{ textAlign: "right", padding: "8px" }}>Time</th>
            </tr>
          </thead>
          <tbody>
            {headlines.map((h, i) => (
              <tr key={i} style={{ borderBottom: "1px solid #1e293b", fontSize: "14px" }}>
                <td style={{ padding: "10px 8px", maxWidth: "500px" }}>
                  <a href={h.url} target="_blank" rel="noreferrer" style={{ color: "#e2e8f0", textDecoration: "none" }}>
                    {h.headline}
                  </a>
                </td>
                <td style={{ textAlign: "center", padding: "10px 8px" }}>
                  <SentimentBadge sentiment={h.sentiment} />
                </td>
                <td style={{ textAlign: "right", padding: "10px 8px", color: h.sentiment_score > 0 ? "#22c55e" : h.sentiment_score < 0 ? "#ef4444" : "#f59e0b" }}>
                  {h.sentiment_score}
                </td>
                <td style={{ textAlign: "right", padding: "10px 8px", color: "#64748b", fontSize: "12px" }}>
                  {new Date(h.published_at).toLocaleTimeString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}