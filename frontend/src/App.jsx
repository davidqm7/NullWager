import { useState } from 'react';
import axios from 'axios';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine 
} from 'recharts';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [finalBalance, setFinalBalance] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const [startCash, setStartCash] = useState(1000);
  const [betSize, setBetSize] = useState(50);
  const [strategy, setStrategy] = useState("flat"); 

  const runSimulation = async () => {
    setLoading(true);
    try {
      const response = await axios.get('https://nullwager-api.onrender.com/simulate', {
        params: { start_cash: startCash, bet_size: betSize, strategy: strategy }
      });
      setData(response.data.history);
      setFinalBalance(response.data.final_balance);
    } catch (error) {
      console.error(error);
      alert("Is the Python backend running?");
    }
    setLoading(false);
  };

  // Helper to format currency
  const fmt = (num) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num);

  return (
    <div style={{ 
      backgroundColor: '#1a1a1a', 
      color: '#e0e0e0', 
      minHeight: '100vh', 
      padding: '40px 20px', 
      fontFamily: '"Inter", sans-serif' 
    }}>
      <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
        
        {/* HEADER */}
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{ fontSize: '3rem', margin: '0', color: '#ff4444', letterSpacing: '-2px' }}>
            NULLWAGER
          </h1>
          <p style={{ color: '#888', marginTop: '10px' }}>The Mathematical Reality of Sports Betting</p>
        </div>

        {/* CONTROLS CARD */}
        <div style={{ 
          backgroundColor: '#2d2d2d', 
          padding: '25px', 
          borderRadius: '12px', 
          boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
          marginBottom: '30px',
          display: 'flex',
          flexWrap: 'wrap',
          gap: '20px',
          alignItems: 'flex-end',
          border: '1px solid #333'
        }}>
          <div>
            <label style={{ display: 'block', color: '#888', fontSize: '12px', marginBottom: '5px' }}>STARTING BANKROLL</label>
            <input 
              type="number" 
              value={startCash} 
              onChange={(e) => setStartCash(Number(e.target.value))}
              style={{ background: '#333', border: '1px solid #555', color: 'white', padding: '10px', borderRadius: '6px', fontSize: '16px' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', color: '#888', fontSize: '12px', marginBottom: '5px' }}>BET SIZE</label>
            <input 
              type="number" 
              value={betSize} 
              onChange={(e) => setBetSize(Number(e.target.value))}
              style={{ background: '#333', border: '1px solid #555', color: 'white', padding: '10px', borderRadius: '6px', fontSize: '16px' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', color: '#888', fontSize: '12px', marginBottom: '5px' }}>STRATEGY</label>
            <select 
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
              style={{ background: '#333', border: '1px solid #555', color: 'white', padding: '10px', borderRadius: '6px', fontSize: '16px', width: '200px' }}
            >
              <option value="flat">Flat Betting (Conservative)</option>
              <option value="martingale">Martingale (Aggressive)</option>
            </select>
          </div>
          <button 
            onClick={runSimulation} 
            disabled={loading}
            style={{
              flex: 1,
              padding: '12px', 
              fontSize: '16px', 
              fontWeight: 'bold',
              backgroundColor: loading ? '#555' : '#ff4444', 
              color: 'white', 
              border: 'none', 
              borderRadius: '6px',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'all 0.2s'
            }}
          >
            {loading ? "CRUNCHING DATA..." : "RUN SIMULATION"}
          </button>
        </div>

        {/* SUMMARY CARD */}
        {finalBalance !== null && (
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(3, 1fr)', 
            gap: '15px', 
            marginBottom: '30px' 
          }}>
            <div className="stat-card" style={{ background: '#2d2d2d', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ color: '#888', fontSize: '12px' }}>FINAL BALANCE</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: finalBalance > startCash ? '#4caf50' : '#ff4444' }}>
                {fmt(finalBalance)}
              </div>
            </div>
            <div className="stat-card" style={{ background: '#2d2d2d', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ color: '#888', fontSize: '12px' }}>NET PROFIT/LOSS</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: (finalBalance - startCash) > 0 ? '#4caf50' : '#ff4444' }}>
                {fmt(finalBalance - startCash)}
              </div>
            </div>
            <div className="stat-card" style={{ background: '#2d2d2d', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ color: '#888', fontSize: '12px' }}>RESULT</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#fff' }}>
                {finalBalance <= 0 ? "💀 BANKRUPT" : "SURVIVED"}
              </div>
            </div>
          </div>
        )}

        {/* GRAPH */}
        {data.length > 0 && (
          <div style={{ height: '400px', width: '100%', background: '#2d2d2d', padding: '20px', borderRadius: '12px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="colorBankroll" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ff4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ff4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis dataKey="game" stroke="#888" />
                <YAxis stroke="#888" />
                <Tooltip contentStyle={{ backgroundColor: '#333', borderColor: '#555', color: '#fff' }} />
                <ReferenceLine y={startCash} stroke="#666" strokeDasharray="3 3" />
                <Area 
                  type="monotone" 
                  dataKey="bankroll" 
                  stroke="#ff4444" 
                  strokeWidth={3}
                  fillOpacity={1} 
                  fill="url(#colorBankroll)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;