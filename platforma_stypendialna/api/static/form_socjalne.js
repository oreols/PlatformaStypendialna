
// Funkcja do dodawania kolejnego wiersza do tabeli
function dodajWiersz() {
    var tabela = document.querySelector('table');
    var tbody = tabela.querySelector('tbody');
    var nowyWiersz = document.createElement('tr');

    nowyWiersz.innerHTML = `
        <td>${tbody.children.length + 1}.</td>
        <td><input type="text" class="imie_nazwisko" placeholder="Imię i nazwisko członka rodziny"></td>
        <td><input type="text" class="pokrewienstwo" placeholder="stopień pokrewieństwa"> <br><input type="date" class="date" placeholder="data urodzenia"></td>
        <td><input type="text" class="miejsce" placeholder="Miejsce pracy lub nauki"></td>
    `;

    tbody.appendChild(nowyWiersz);
}
var przyciskDodaj = document.getElementById('przycisk_dodaj_wiersz');

przyciskDodaj.addEventListener('click', dodajWiersz);


//dodawanie elementu do listy 
function dodajElementListy() {
    
    var lista = document.querySelector('.inne_dochody ul');

    var nowyElement = document.createElement('li');

    nowyElement.innerHTML = `
        Imie i nazwisko : <input type="text" class="imie_nazwisko_czlonka"> <br>
        Rodzaj uzyskiwanego dochodu: <input type="text" class="rodzaj_dochodu"> <br>
        Kwota dochodu: <input type="number" class="kwota_dochodu">
    `;

   
    lista.appendChild(nowyElement);
}


var przyciskDodaj = document.getElementById('przycisk_dodaj_element_listy');


if (przyciskDodaj) {
    przyciskDodaj.addEventListener('click', dodajElementListy);
}

//sumowanie dochodów
var sumaDochoduGosp = document.getElementById('suma_dochodu_gosp');
        var sumaInnychDoch = document.getElementById('suma_innych_doch');
        var lacznaKwotaDoch = document.getElementById('laczna_kwota_doch');

        if (sumaDochoduGosp && sumaInnychDoch && lacznaKwotaDoch) {
            sumaDochoduGosp.addEventListener('input', obliczLacznaKwoteDoch);
            sumaInnychDoch.addEventListener('input', obliczLacznaKwoteDoch);
        }

        
        function obliczLacznaKwoteDoch() {
            
            var dochodGosp = parseFloat(sumaDochoduGosp.value) || 0;
            var dochodInne = parseFloat(sumaInnychDoch.value) || 0;
    
            var lacznaKwota = dochodGosp + dochodInne;

            lacznaKwotaDoch.value = lacznaKwota.toFixed(2);
        }