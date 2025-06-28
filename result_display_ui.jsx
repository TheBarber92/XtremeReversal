import React from "react";

export default function ResultDisplay({ userId, timestamp, resultData, imageUrl }) {
  return (
    <div className="min-h-screen bg-white text-black p-4">
      <header className="mb-4">
        <h1 className="text-2xl font-bold">XtremeReversal Result</h1>
        <a href="/" className="text-blue-600 underline text-sm">&larr; Back to Upload</a>
      </header>

      <section className="mb-6">
        <p><strong>User ID:</strong> #{userId}</p>
        <p><strong>Upload Time:</strong> {timestamp}</p>
      </section>

      <section className="mb-6">
        <img src={imageUrl} alt="Uploaded Chart" className="max-w-md border rounded shadow" />
        <div className="mt-2">
          <a href={imageUrl} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline text-sm">🔍 View Fullscreen</a>
        </div>
      </section>

      <section className="mb-6">
        <h2 className="text-xl font-semibold mb-2">Analysis Result</h2>
        <div className="border p-4 rounded bg-gray-100">
          <p><strong>Setup Status:</strong> {resultData.status}</p>
          {resultData.tp && (
            <ul className="list-disc list-inside ml-4">
              <li>TP1: {resultData.tp.tp1}</li>
              <li>TP2: {resultData.tp.tp2}</li>
              <li>TP3: {resultData.tp.tp3}</li>
            </ul>
          )}
        </div>
      </section>

      <section className="mb-6">
        <button className="px-4 py-2 bg-blue-600 text-white rounded mr-2">⬇ Save as PDF</button>
        <button className="px-4 py-2 bg-gray-700 text-white rounded">📤 Share Result Link</button>
      </section>

      <footer className="border-t pt-4">
        <button className="text-blue-600 underline mr-4">← Upload Another Screenshot</button>
        <button className="text-blue-600 underline">🔍 View My History</button>
      </footer>
    </div>
  );
}
