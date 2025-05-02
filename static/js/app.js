document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    try {
        const response = await fetch("/process", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            // Display results
            document.getElementById("result").style.display = "block";
            document.getElementById("extractedText").textContent = result.extracted_text || "N/A";
            document.getElementById("translatedText").textContent = result.translated_text || "N/A";

            // Display the watermarked image
            const outputImage = document.getElementById("outputImage");
            outputImage.src = result.output_image;
            outputImage.style.display = "block";

            // Display the translated text image
            const textImage = document.getElementById("textImage");
            textImage.src = result.text_image;
            textImage.style.display = "block";
        } else {
            alert(result.error || "An error occurred while processing the image.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An unexpected error occurred.");
    }
});