delete_buttons = document.querySelectorAll(".btn-delete");
form = document.querySelector(".form-delete");

delete_buttons.forEach((btn) => {
  btn.addEventListener("click", () => {
    deleteBtn = document.querySelector(".delete-btn");
    time_count = document.querySelector("#time");
    delete_p = document.querySelector("#delete-p");
    cancelBtn = document.querySelector(".btnCancel");

    seconds = 2;

    console.log(form.action);

    form.action = form.action + btn.id;
    interval = setInterval(() => {
      time_count.textContent = seconds;
      seconds--;
    }, 1000);

    cancelBtn.addEventListener("click", () => {
      delete_p.innerHTML = 'Wait... <span id="time">3</span> sec.';
      seconds = 2;
      clearInterval(interval);
    });

    setTimeout(() => {
      deleteBtn.disabled = false;
      clearInterval(interval);
      delete_p.textContent = "Category remove enabled";
      time_count.textContent = "";
    }, 3000);
  });
});
