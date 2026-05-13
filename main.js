document.getElementById("findBtn").addEventListener("click", findRoute);

let isLoading = false;

async function findRoute() {
    if (isLoading) return; // prevent spam clicks
    isLoading = true;

    const startRaw = document.getElementById("start").value.trim();
    const goalRaw = document.getElementById("goal").value.trim();

    const statusDiv = document.getElementById("status");
    const resultDiv = document.getElementById("result");

    const start = startRaw.toLowerCase().replace(/\s+/g, "_");
    const goal = goalRaw.toLowerCase().replace(/\s+/g, "_");

    if (!start || !goal) {
        statusDiv.innerText = "Please enter both locations.";
        isLoading = false;
        return;
    }

    statusDiv.innerText = "Searching best route (A*)...";
    resultDiv.innerText = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/route", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ start, goal })
        });

        const data = await response.json();

        if (!response.ok || data.error) {
            statusDiv.innerText = "❌ " + (data.error || "Server error");
            isLoading = false;
            return;
        }

        if (data.path && Array.isArray(data.path)) {
            const costText = data.cost !== undefined
                ? Number(data.cost).toFixed(4)
                : "N/A";

            resultDiv.innerText =
                "✅ Path: " + data.path.join(" → ") +
                "\nCost: " + costText;

            statusDiv.innerText = "Route found!";

            if (typeof drawRoute === "function") {
                drawRoute(data.path);
            }

        } else {
            resultDiv.innerText = "No path found.";
            statusDiv.innerText = "";
        }

    } catch (err) {
        statusDiv.innerText = "⚠️ Cannot connect to backend. Is Flask running?";
        console.error(err);
    }

    isLoading = false;
}