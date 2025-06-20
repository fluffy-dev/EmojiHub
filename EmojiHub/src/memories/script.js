// script.js — финальная версия

document.addEventListener("DOMContentLoaded", () => {
  const user = localStorage.getItem("emojiUser") || "guest";
  const container = document.getElementById("emojiContainer");
  const searchInput = document.getElementById("searchInput");
  const categorySelect = document.getElementById("categorySelect");
  let emojisData = [];

  async function loadEmojis() {
    try {
      const res = await fetch("https://emojihub.yurace.pro/api/all");
      emojisData = await res.json();

      const categories = [...new Set(emojisData.map(e => e.category))].sort();
      categories.forEach(cat => {
        const option = document.createElement("option");
        option.value = cat;
        option.textContent = cat;
        categorySelect.appendChild(option);
      });

      displayEmojis(emojisData);
      searchInput.addEventListener("input", applyFilters);
      categorySelect.addEventListener("change", applyFilters);
    } catch (err) {
      container.innerHTML = "<p>😞 Failed to load emojis.</p>";
      console.error(err);
    }
  }

  function applyFilters() {
    const query = searchInput.value.toLowerCase();
    const selectedCategory = categorySelect.value;

    const filtered = emojisData.filter(e => {
      const matchName = e.name.toLowerCase().includes(query);
      const matchCat = selectedCategory === "all" || e.category === selectedCategory;
      return matchName && matchCat;
    });

    displayEmojis(filtered);
  }

  function displayEmojis(emojis) {
    container.innerHTML = "";

    fetch(`http://localhost:5050/favorites/${user}`)
      .then(res => res.json())
      .then(favs => {
        emojis.forEach(e => {
          const card = document.createElement("div");
          card.className = "emoji-card";

          const emojiChar = e.htmlCode[0];
          const name = e.name;
          const isFav = favs.includes(name);

          card.innerHTML = `
            <div style="font-size: 2rem;">${emojiChar}</div>
            <small>${name}</small><br>
            <button class="fav-btn">${isFav ? "❤️" : "🤍"}</button>
          `;

          const favBtn = card.querySelector(".fav-btn");

          favBtn.onclick = (event) => {
            event.stopPropagation();
            const action = favBtn.textContent === "❤️" ? "DELETE" : "POST";

            fetch(`http://localhost:5050/favorites/${user}`, {
              method: action,
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ name })
            })
            .then(res => res.json())
            .then(() => {
              favBtn.textContent = action === "POST" ? "❤️" : "🤍";
            })
            .catch(err => {
              console.error("Ошибка при добавлении/удалении из избранного:", err);
            });
          };

          card.onclick = (event) => {
            if (event.target.tagName === "BUTTON") return;
            localStorage.setItem("emojiDetails", JSON.stringify(e));
            window.location.href = "emoji-details.html";
          };

          container.appendChild(card);
        });
      });
  }

  loadEmojis();
});
