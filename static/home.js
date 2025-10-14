// document.getElementById("extractBtn").addEventListener("click", async () => {
//   const text = document.getElementById("inputText").value;
//   const response = await fetch("http://127.0.0.1:5000/get-data", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body: JSON.stringify({ text })
//   });
//   const data = await response.json();

//   // display results
//   const outputDiv = document.getElementById("output");
//   outputDiv.innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
// });


fetch("/api/data")
    .then(response => response.json())
    .then(data => {
      const template = document.getElementById("grant-template");
      const tableBody = document.getElementById("grants-body")
      const modal = document.getElementById("modal");
      const modalText = document.getElementById("modal-text");
      const closeModal = modal.querySelector(".close");

      console.log(data);

      data.forEach(grant => {
        const clone = template.content.cloneNode(true);

        clone.querySelector(".title").textContent = grant.title;
        clone.querySelector(".amount").textContent = grant.amount ? grant.amount.join(", ") : "N/A";
        clone.querySelector(".open-date").textContent = grant.open_date || "TBD";
        clone.querySelector(".close-date").textContent = grant.close_date || "TBD";
        clone.querySelector(".requirements").textContent = grant.Requirements || "...";
        clone.querySelector(".description").textContent = grant.Description || "...";
        
        const readMoreBtns = clone.querySelectorAll(".read-more");
        readMoreBtns.forEach(button => {
          button.addEventListener("click", () => {
            const type = button.dataset.type;
            const text = type === "requirements" ? grant.Requirements : grant.Description;

            if(grant.link){
              modalText.innerHTML = `<p> ${text}</p> <a href="${grant.link}" target="_blank" rel="noopener noreferrer">Learn more</a>`;
            }
            else{
              modalText.textContent = text || "n/a";
            }
            modal.style.display = "block";
          });
        });

        tableBody.appendChild(clone);
      });

            closeModal.addEventListener("click", () => {
        modal.style.display = "none";
      })

      window.addEventListener("click", (e) => {
        if (e.target === modal){
          modal.style.display = "none";
        }
      })
    });