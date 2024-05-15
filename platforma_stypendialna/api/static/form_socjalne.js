document.addEventListener('DOMContentLoaded', function () {
    let addButton = document.getElementById('przycisk_dodaj_wiersz');
    let tableBody = document.getElementById('familyMembersTable');
    let totalForms = document.querySelector('input[name="form-TOTAL_FORMS"]');
    let rowCount = parseInt(totalForms.value);

    addButton.addEventListener('click', function (event) {
        event.preventDefault();  // Zapobiega wysłaniu formularza
        let newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${rowCount + 1}</td>
            <td><input type="text" name="form-${rowCount}-imie_czlonka" placeholder="Imię">
                <input type="text" name="form-${rowCount}-nazwisko_czlonka" placeholder="Nazwisko"></td>
            <td><input type="text" name="form-${rowCount}-stopien_pokrewienstwa" placeholder="Stopień pokrewieństwa">
                <input type="date" name="form-${rowCount}-data_urodzenia"></td>
            <td><input type="text" name="form-${rowCount}-miejsce_pracy" placeholder="Miejsce pracy lub nauki"></td>
        `;
        tableBody.appendChild(newRow);
        rowCount++;
        totalForms.value = rowCount;
    });
});
