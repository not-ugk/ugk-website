const songs = require('./data.json')
const Fuse = require('fuse.js')

const fuseOptions = {
    keys: ['artist', 'title'],
    isCaseSensitive: false,
    threshold: 0.1
}

const search = new Fuse(songs, fuseOptions)

const Maskito = require('@maskito/core')
const maskedInput = new Maskito.Maskito(
    document.getElementById("search"), {
        preprocessors: [
            ({elementState, data}, _) => {
                executesearchwithterm(elementState.value);
                return(elementState, data)
            }
        ]
    }
)

export function executesearch() {
    clearResults();
    executesearchwithterm(document.getElementById("search").value)
}

function executesearchwithterm(searchterm) {
    clearResults();
    console.log("Searching artists:" + searchterm)
    const result = search.search(searchterm)
    console.log(result)
    result.forEach(element => appendToResults(element.item))
}

export function random() {
    clearResults();
    console.log('producing random song')
    const song = getRandomSong();
    console.log('random song is ' + song);
    appendToResults(song);
}

function clearResults() {
    var results = document.getElementById('results')
    while (results.firstChild) {
        results.removeChild(results.firstChild)
    }
}

function appendToResults(newItem) {
    console.log("appending item: " + newItem)
    const results = document.getElementById('results');
    results.appendChild(newRow(newItem.artist, newItem.title));
}

function newRow(artist, song) {
    const tr = document.createElement('tr')
    const td1 = document.createElement('th')
    td1.appendChild(document.createTextNode(artist))
    const td2 = document.createElement('td')
    td2.appendChild(document.createTextNode(song))
    tr.appendChild(td1)
    tr.appendChild(td2)
    return tr
}

function getRandomSong() {
    return songs[Math.floor(Math.random() * songs.length)]
}