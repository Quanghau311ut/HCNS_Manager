document.addEventListener('click', function (event) {
  const opener = event.target.closest('[data-open-modal]');
  if (opener) {
    const modal = document.getElementById(opener.dataset.openModal);
    if (modal) modal.classList.add('open');
  }
  if (event.target.closest('.close-modal')) {
    const modal = event.target.closest('.modal-backdrop');
    if (modal) modal.classList.remove('open');
  }
  if (event.target.classList.contains('modal-backdrop')) event.target.classList.remove('open');
  const edit = event.target.closest('.edit-button');
  if (edit) {
    document.getElementById('modal-title').textContent = 'Cập nhật thông tin';
    document.getElementById('record-id').value = edit.dataset.id;
    document.getElementById('record-title').value = edit.dataset.title;
    document.getElementById('record-detail').value = edit.dataset.detail;
    document.getElementById('record-status').value = edit.dataset.status;
    document.getElementById('record-start').value = edit.dataset.start;
    document.getElementById('record-end').value = edit.dataset.end;
    document.getElementById('record-owner').value = edit.dataset.owner;
    document.getElementById('record-modal').classList.add('open');
  }
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') document.querySelectorAll('.modal-backdrop.open').forEach(modal => modal.classList.remove('open'));
});
const search = document.getElementById('table-search');
const filter = document.getElementById('status-filter');
function filterRows() {
  const query = search ? search.value.trim().toLocaleLowerCase('vi') : '';
  const status = filter ? filter.value : '';
  document.querySelectorAll('#data-table tbody tr[data-status]').forEach(row => {
    row.hidden = (status && row.dataset.status !== status) || (query && !row.textContent.toLocaleLowerCase('vi').includes(query));
  });
}
if (search) search.addEventListener('input', filterRows);
if (filter) filter.addEventListener('change', filterRows);
