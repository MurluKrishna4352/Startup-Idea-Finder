const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchIdeas(query) {
  const res = await fetch(`${API_URL}/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) {
    throw new Error("Failed to fetch ideas");
  }

  return res.json();
}

export async function downloadPDF(query) {
  const res = await fetch(`${API_URL}/generate-pdf`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) {
    throw new Error("Failed to generate PDF");
  }

  // Return a Blob so frontend can download it
  const blob = await res.blob();
  return blob;
}
