import { useState } from 'react';
import ReactMarkdown from 'react-markdown'; // نئی لائبریری امپورٹ کریں
import './App.css';

function App() {
  const [productName, setProductName] = useState('');
  const [keywords, setKeywords] = useState('');
  const [platform, setPlatform] = useState('Amazon');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const generateAIContent = async () => {
    if (!productName || !keywords) {
      alert("Please fill all fields!");
      return;
    }

    setLoading(true);
    setDescription(''); // نیا جواب آنے سے پہلے پرانا صاف کر دیں

    try {
      // بیک اینڈ کا لنک یہاں سیٹ کریں (لائیو کرنے کے بعد اسے بدلنا ہوگا)
      const response = await fetch('http://127.0.0.1:8000/generate-description', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_name: productName,
          keywords: keywords,
          platform: platform
        }),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setDescription(data.description);
    } catch (error) {
      setDescription(`Error: Could not connect to backend. **Make sure your Python server is running on port 8000.**\n\n*Technical Details: ${error.message}*`);
    }
    setLoading(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(description);
    alert("Professional description copied! ✅");
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI Product Description Assistant</h1>
        <p>Get professional SEO-optimized descriptions in seconds.</p>
      </header>
      
      <div className="input-panel">
        <label>Product Name</label>
        <input 
          type="text" 
          placeholder="e.g. Smart Watch Series 7" 
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
        />
        
        <label>Primary Keywords</label>
        <input 
          type="text" 
          placeholder="e.g. waterproof, bluetooth, sleek design" 
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
        />
        
        <label>Target Platform</label>
        <select value={platform} onChange={(e) => setPlatform(e.target.value)}>
          <option value="Amazon">Amazon</option>
          <option value="eBay">eBay</option>
          <option value="Shopify">Shopify</option>
          <option value="Etsy">Etsy</option>
        </select>

        <button onClick={generateAIContent} disabled={loading} className="generate-btn">
          {loading ? 'Thinking...' : 'Generate Description'}
        </button>
      </div>

      {description && (
        <div className="result-panel">
          <div className="result-header">
            <h3>Generated for {platform}:</h3>
            <button onClick={copyToClipboard} className="copy-btn">
              📋 Copy Raw Text
            </button>
          </div>
          
          <div className="markdown-display">
            {/* یہیں وہ جادوئی لائبریری ٹیکسٹ کو خوبصورت بنا رہی ہے */}
            <ReactMarkdown>{description}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;