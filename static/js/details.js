let { fileName, isSafe, fileSize, fileType, checkDate } = JSON.parse(
  localStorage.getItem("file")
);
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
