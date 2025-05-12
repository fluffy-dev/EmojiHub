// favorites.js с анимацией загрузки

document.addEventListener("DOMContentLoaded", async () => {
  const user = localStorage.getItem("emojiUser") || "guest";
  const container = document.getElementById("favoritesContainer");

  // Добавляем анимацию загрузки
  container.innerHTML = "<p style='text-align:center; font-style:italic;'>Loading your favorite emojis... ⏳</p>";

  try {
    const res = await fetch(`http://localhost:5050/favorites/${user}`);
    const favoriteNames = await res.json();

    if (favoriteNames.length === 0) {
      container.innerHTML = "<p>No favorites yet 😢</p>";
      return;
    }

    const allRes = await fetch("emojis.json");
    const allEmojis = await allRes.json();
    const filtered = allEmojis.filter(e => favoriteNames.includes(e.name));

    container.innerHTML = "";

    filtered.forEach(e => {
      const card = document.createElement("div");
      card.className = "emoji-card";

      card.innerHTML = `
        <div style="font-size: 2rem;">${e.htmlCode[0]}</div>
        <small>${e.name}</small><br>
        <button class="remove-btn">❌ Remove</button>
        <button class="info-btn">ℹ️</button>
      `;

      card.querySelector(".remove-btn").onclick = () => {
        fetch(`http://localhost:5050/favorites/${user}`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name: e.name })
        }).then(() => location.reload());
      };

      card.querySelector(".info-btn").onclick = () => {
        localStorage.setItem("emojiDetails", JSON.stringify(e));
        window.location.href = "emoji-details.html";
      };

      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = "<p>⚠️ Failed to load favorites.</p>";
    console.error(err);
  }
});

function exportFavorites() {
  const user = localStorage.getItem("emojiUser") || "guest";

  fetch(`http://localhost:5050/favorites/${user}`)
    .then(res => res.json())
    .then(async favNames => {
      const res = await fetch("emojis.json");
      const allEmojis = await res.json();

      const filtered = allEmojis.filter(e => favNames.includes(e.name));

      const blob = new Blob([JSON.stringify(filtered, null, 2)], {
        type: "application/json"
      });

      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `${user}_favorites.json`;
      a.click();
      URL.revokeObjectURL(a.href);
    })
    .catch(err => {
      console.error("Export failed:", err);
      alert("⚠️ Could not export favorites.");
    });
}

document.getElementById("importInput").addEventListener("change", async function(event) {
  const file = event.target.files[0];
  if (!file) return;

  try {
    const text = await file.text();
    const imported = JSON.parse(text);
    const user = localStorage.getItem("emojiUser") || "guest";

    for (const emoji of imported) {
      await fetch(`http://localhost:5050/favorites/${user}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: emoji.name })
      });
    }

    alert("✅ Imported successfully!");
    location.reload();
  } catch (err) {
    console.error("Import failed:", err);
    alert("⚠️ Failed to import. Invalid file?");
  }
});
