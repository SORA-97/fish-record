document.addEventListener("DOMContentLoaded", () => {
    const filter = document.getElementById("filter");
    const filter_detail = document.getElementById("filter-detail");
  
    filter.addEventListener("change", () => {
      const selectedValue = filter.value;
  
      filter_detail.innerHTML = '<option value="">絞りこみなし</option>';
      filter_detail.disabled = true;
  
      if (selectedValue) {
        fetch("/get_details", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ option: selectedValue })
        })
          .then(response => response.json())
          .then(data => {
            const details = data.details;
            if (details.length > 0) {
              for (let i = 0; i < details.length; i++) {
                const option = document.createElement("option");
                option.value = details[i];
                option.textContent = details[i];
                filter_detail.appendChild(option);
              }
              filter_detail.disabled = false;
            }
          })
          .catch(error => console.error("Error:", error));
      }
    });
  });
  