document.getElementById("image-selection").addEventListener("change", function(e) {
    const selectedCategory = e.target.value;
    // Select all image containers in the grid
    const imageDivs = document.querySelectorAll(".grid > div");
    
    imageDivs.forEach(div => {
        const category = div.getAttribute("category");
        if (selectedCategory === "all" || category === selectedCategory) {
            div.style.display = ""; // Show the div (default display)
        } else {
            div.style.display = "none"; // Hide the div
        }
    });
});