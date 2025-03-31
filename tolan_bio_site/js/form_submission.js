document.getElementById("contactForm").addEventListener("submit",function(event){
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    console.log("this.action: ", this.action)
    fetch(this.action, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success: ",  data)
        alert("Form submitted successfully!");
        this.reset()
        
    })
    .catch(error => {
        console.log("Error: ", error)
        alert("Submission failed!");
    })
});