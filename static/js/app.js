document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData();
    const imageFile = document.getElementById("image").files[0];
    formData.append("image", imageFile);

    try {
        const response = await fetch("/process", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Failed to process the image.");
        }

        const result = await response.json();

        // Display results
        document.getElementById("result").style.display = "block";
        document.getElementById("extractedText").textContent = result.extracted_text || "N/A";
        document.getElementById("translatedText").textContent = result.translated_text || "N/A";

        const outputImage = document.getElementById("outputImage");
        outputImage.src = result.output_image;
        outputImage.style.display = "block";
    } catch (error) {
        alert("An error occurred: " + error.message);
    }
});