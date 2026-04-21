import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// واجد، یہ رہا آپ کا لائیو بیک اینڈ لنک
const API_URL = "https://ai-product-assistant-psi.vercel.app";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // صارف کا میسج سکرین پر دکھائیں
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      // یہاں آپ کا فرنٹ اینڈ لائیو بیک اینڈ سے بات کر رہا ہے
      const response = await axios.post(`${API_URL}/chat`, {
        message: input
      });

      // AI کا جواب سکرین پر دکھائیں
      // یہاں response کی جگہ description لکھیں
setMessages([...newMessages, { role: "assistant", content: response.data.description }]);
    } catch (error) {
      console.error("Error connecting to backend:", error);
      setMessages([...newMessages, { role: "assistant", content: "معذرت، بیک اینڈ سے رابطہ نہیں ہو سکا۔ براہ کرم چیک کریں کہ API Key ایڈ ہے یا نہیں۔" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Product Assistant</h1>
        <div className="chat-window">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <strong>{msg.role === "user" ? "You: " : "AI: "}</strong>
              {msg.content}
            </div>
          ))}
          {loading && <p className="loading">AI سوچ رہا ہے...</p>}
        </div>
        <form onSubmit={sendMessage} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="اپنا سوال یہاں لکھیں..."
          />
          <button type="submit" disabled={loading}>Send</button>
        </form>
      </header>
    </div>
  );
}

export default App;