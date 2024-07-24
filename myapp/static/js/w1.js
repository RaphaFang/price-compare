"use strict";
document.addEventListener("DOMContentLoaded", async function () {
  await getDownload();
});

const ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif"];

async function postUpload() {
  const textContent = document.getElementById("text-content").value;
  const fileUpload = document.getElementById("file-upload").files[0];

  if (!textContent) {
    alert("Must upload at least one piece of message.");
    return;
  }
  if (fileUpload) {
    if (!ALLOWED_IMAGE_TYPES.includes(fileUpload.type)) {
      alert("Only jpg/png/gif files are allowed");
      return;
    }
  }
  if (fileUpload && fileUpload.size > 10 * 1024 * 1024) {
    alert("Please make sure the size of the file is smaller then 10mb.");
    return;
  }

  const form = document.getElementById("upload-form");
  const formData = new FormData(form);
  try {
    const response = await fetch("/task/v1/api/upload", {
      method: "POST",
      body: formData,
    });
    console.log("Response status:", response.status);
    console.log("Response headers:", response.headers);

    const result = await response.json();
    if (response.ok) {
      console.log("Success:", result);
      await getDownload();
      alert("Upload successfully!");
    } else {
      console.error("Error:", result);
      alert("Upload failed...");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error happened, check the back end.");
  }
}

async function getDownload() {
  try {
    const response = await fetch("/task/v1/api/download", {
      method: "GET",
    });
    const result = await response.json();

    if (response.ok) {
      console.log("Success:", result.data);
      render(result.data);
    } else {
      console.error("Error:", result);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

function render(d) {
  const belowDiv = document.getElementById("info-below");
  belowDiv.innerHTML = "";
  for (let n = 0; n < d.length; n++) {
    if (d[n]["pic"] !== null) {
      belowDiv.innerHTML += `
          <div class="block">
            <div class="img-container">
              <img src="${d[n]["pic"]}" alt="Image" class="user-pic lazy" />
            </div>
            <div class="text-div">
              <p>${d[n]["text"]}</p>
            </div>
          </div>`;
    } else {
      belowDiv.innerHTML += `
          <div class="block">
            <div class="img-container">
            </div>
            <div class="text-div">
              <p>${d[n]["text"]}</p>
            </div>
          </div>`;
    }
  }
}
