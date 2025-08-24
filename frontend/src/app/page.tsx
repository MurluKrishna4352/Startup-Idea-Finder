"use client";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function Home() {
  const [subreddit, setSubreddit] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [summary, setSummary] = useState("");
  const [solutions, setSolutions] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSummary("");
    setSolutions("");
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/scrape/${encodeURIComponent(subreddit)}?limit=5`
      );
      if (!res.ok) {
        throw new Error("Subreddit not found or backend error.");
      }
      const data = await res.json();
      setSummary(data.summary);
      setSolutions(data.solutions);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unknown error");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    window.open(`${process.env.NEXT_PUBLIC_API_URL}/download/pdf`, "_blank");
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 p-4">
      <div className="max-w-xl w-full bg-gray-100 rounded-2xl shadow-2xl p-8 flex flex-col items-center">
        <h1 className="text-4xl font-extrabold mb-8 text-center text-blue-700">
          Reddit Research Bot
        </h1>
        <form
          className="w-full flex flex-col items-center gap-4"
          onSubmit={handleSubmit}
        >
          <input
            type="text"
            value={subreddit}
            onChange={(e) => setSubreddit(e.target.value)}
            placeholder="Enter subreddit (e.g. python)"
            className="w-full px-4 py-3 border border-blue-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900 text-lg"
            required
          />
          <button
            type="submit"
            className="w-full bg-blue-700 text-white py-3 rounded-lg font-bold hover:bg-blue-800 transition text-lg shadow"
            disabled={loading}
          >
            {loading ? "Scraping..." : "Scrape"}
          </button>
        </form>

        {loading && (
          <div className="flex justify-center items-center mt-8">
            <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-b-4 border-blue-700"></div>
          </div>
        )}

        {error && (
          <div className="mt-8 text-red-700 font-bold text-center text-lg">
            {error}
          </div>
        )}

        {summary && (
          <div className="mt-10 w-full">
            <h2 className="text-2xl font-bold mb-4 text-blue-700">Summary</h2>
            <div className="mb-8 prose prose-lg max-w-none bg-white p-4 rounded-xl shadow text-gray-900">
              <ReactMarkdown>{summary}</ReactMarkdown>
            </div>
          </div>
        )}

        {solutions && (
          <div className="mt-8 w-full">
            <h2 className="text-2xl font-bold mb-4 text-blue-700">Solutions</h2>
            <div className="prose prose-lg max-w-none bg-white p-4 rounded-xl shadow text-gray-900">
              <ReactMarkdown>{solutions}</ReactMarkdown>
            </div>
            <button
              onClick={handleDownload}
              className="mt-8 w-full bg-blue-700 text-white py-3 rounded-lg font-bold hover:bg-blue-800 transition text-lg shadow"
            >
              Download PDF
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
