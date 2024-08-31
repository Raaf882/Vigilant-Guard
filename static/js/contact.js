const contactFormBtn = document.getElementById("contactFormBtn");
const okBtn = document.getElementById("okBtn");
const contactDataResault = document.getElementById("contactDataResault");
const formData = document.getElementById("formData");

AOS.init();

contactFormBtn.addEventListener('click',function(){
    formData.classList.add("data-form-hidden")
    formData.reset();
    contactDataResault.classList.remove("data-form-resault-hidden")

})
okBtn.addEventListener('click',function(){
    formData.classList.remove("data-form-hidden")
    contactDataResault.classList.add("data-form-resault-hidden")
})