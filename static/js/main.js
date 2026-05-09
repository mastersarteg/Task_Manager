document.addEventListener('DOMContentLoaded', () => {
  const toastElList = Array.from(document.querySelectorAll('.toast'));
  toastElList.forEach(toastEl => {
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  });
});
