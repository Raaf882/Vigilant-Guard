AOS.init();

const uploadLabel = document.getElementById("uploadLabel");
const submitBtn = document.getElementById("formBtn");
const fileInput = document.getElementById("uploadFile");
uploadLabel.addEventListener("dragenter", highlightLabel);
uploadLabel.addEventListener("dragleave", unhighlightLabel);
uploadLabel.addEventListener("dragover", preventDefault);
uploadLabel.addEventListener("drop", handleFileDrop);
fileInput.addEventListener("change", handleFileSelection);

function highlightLabel(event) {
  event.preventDefault();
  uploadLabel.classList.add("highlight");
}

function unhighlightLabel(event) {
  event.preventDefault();
  uploadLabel.classList.remove("highlight");
}

function preventDefault(event) {
  event.preventDefault();
}

function handleFileDrop(event) {
  event.preventDefault();
  uploadLabel.classList.remove("highlight");
  const files = event.dataTransfer.files;

  dataResault.innerHTML = "";

  if (files.length > 0) {
    handleFiles(files);
  }
}

function handleFileSelection() {
  const files = fileInput.files;

  dataResault.innerHTML = "";

  if (files.length > 0) {
    handleFiles(files);
  }
}

function handleFiles(files) {
  const repoHeader = document.createElement("div");
  repoHeader.classList.add("repo-header");
  repoHeader.innerHTML = "<h3>Report</h3>";
  dataResault.appendChild(repoHeader);

  const checkingHTML = generateCheckingHTML();
  uploadLabel.innerHTML = checkingHTML;

  checkFiles(files);
}

function generateCheckingHTML() {
  return `
      <div class="check_file">
        <img src="static/images/check.jpg" alt="check" />
        <span>Checking file...</span>
      </div>`;
}

function checkFiles(files) {
  let filesChecked = 0;

  const formData = new FormData();
  for (const file of files) {
    formData.append("file", file);
  }

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      const predictions = data.prediction;
      for (let i = 0; i < files.length; i++) {
        const currentFile = files[i];
        setTimeout(() => {
          let isSafe;
          if (predictions[i] === 0) {
            isSafe = 1;
          } else {
            isSafe = 0;
          }
          // const isSafe = predictions[i];
          uploadLabel.innerHTML += generateResultHTML(isSafe, currentFile.name);

          addFileDetailsToDiv(
            currentFile.name,
            isSafe,
            currentFile.size,
            currentFile.type,
            new Date()
          );
          filesChecked++;
          if (filesChecked === files.length) {
            updateSubmitButton();
            const checkingDiv = document.querySelector(".check_file");
            checkingDiv.style.display = "none";
          }
        }, 1000 * (i + 1));
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function generateResultHTML(isSafe, fileName) {
  const resultClass = isSafe ? "safe-file" : "files-with-virus";
  const resultImage = isSafe
    ? "static/images/true.png"
    : "static/images/false.png";
  const progressBarColor = isSafe ? "bg-primary" : "bg-danger";
  const longBar = isSafe ? "100" : "75";

  return `
      <div class="resault">
        <div class="file-name-title">
          <span>File Name</span>
          <h4>${fileName}</h4>
        </div>
        <div class="files ${resultClass}">
          <h6 class="file-name">${fileName}</h6>
          <div class="resault-bar">
            <i class="fa-regular fa-file-lines"></i>
            <div
              class="progress"
              role="progressbar"
              aria-label="Danger example"
              aria-valuenow="100"
              aria-valuemin="0"
              aria-valuemax=${longBar}
            >
              <div class="progress-bar ${progressBarColor}" style="width: ${longBar}%">${longBar}%</div>
            </div>
            <img src="${resultImage}" />
          </div>
        </div>
      </div>`;
}

function addFileDetailsToDiv(fileName, isSafe, fileSize, fileType, checkDate) {
  localStorage.removeItem("file");
  let fileDetails = {
    fileName,
    isSafe,
    fileSize,
    fileType,
    checkDate,
  };
  localStorage.setItem("file", JSON.stringify(fileDetails));
  const result = isSafe ? "Clean" : "Infected";
  const resaultCell = document.createElement("div");
  resaultCell.classList.add("resault-cell");

  const resTitle = document.createElement("div");
  resTitle.classList.add("res-title");
  resTitle.innerHTML = `<span>File Name</span>`;
  resaultCell.appendChild(resTitle);

  const resDataFileName = document.createElement("div");
  resDataFileName.classList.add("res-data");
  resDataFileName.innerHTML = `<span>${fileName}</span>`;
  resaultCell.appendChild(resDataFileName);

  dataResault.appendChild(resaultCell);

  addFileDetailToDiv("Result", result);
  addFileDetailToDiv("File Size", fileSize);
  addFileDetailToDiv("File Type", fileType);
  addFileDetailToDiv("Check Date", checkDate.toLocaleString());
}

function addFileDetailToDiv(detailTitle, detailValue) {
  const resaultCell = document.createElement("div");
  resaultCell.classList.add("resault-cell");

  const resTitle = document.createElement("div");
  resTitle.classList.add("res-title");
  resTitle.innerHTML = `<span>${detailTitle}</span>`;
  resaultCell.appendChild(resTitle);

  const resData = document.createElement("div");
  resData.classList.add("res-data");
  resData.innerHTML = `<span>${detailValue}</span>`;
  resaultCell.appendChild(resData);

  dataResault.appendChild(resaultCell);
}

function updateSubmitButton() {
  setTimeout(() => {
    submitBtn.innerHTML = '<a href="details">Show Details</a>';
  }, 0);
}

submitBtn.addEventListener("click", function () {
  dataResault.innerHTML = "";
  formData.classList.add("data-form-hidden");
  formData.reset();
  dataResault.classList.remove("data-form-resault-hidden");
});

const contactFormBtn = document.getElementById("contactFormBtn");
const okBtn = document.getElementById("okBtn");
const contactDataResault = document.getElementById("contactDataResault");
const formData = document.getElementById("formData");

contactFormBtn.addEventListener("click", function () {
  formData.classList.add("data-form-hidden");
  formData.reset();
  contactDataResault.classList.remove("data-form-resault-hidden");
});

okBtn.addEventListener("click", function () {
  formData.classList.remove("data-form-hidden");
  contactDataResault.classList.add("data-form-resault-hidden");
});
