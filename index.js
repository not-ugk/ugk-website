const songs = require('./data.json')
const Fuse = require('fuse.js')

const fuseOptions = {
    keys: ['artist', 'title'],
    isCaseSensitive: false,
    threshold: 0.2,
    location: 22,
    distance: 1000,
    shouldSort: false
}

const resultsHead = document.getElementById("results-head")
resultsHead.style.display === "none"
const results = document.getElementById('results')
fullSongList()


const search = new Fuse(songs, fuseOptions)

const Maskito = require('@maskito/core')
const maskedInput = new Maskito.Maskito(
    document.getElementById("search"), {
        preprocessors: [
            ({elementState, data}, _) => {
                if (elementState.value === "") {
                    fullSongList()
                } else {
                    executesearchwithterm(elementState.value);
                }
                return(elementState, data)
            }
        ]
    }
)

function fullSongList() {
    clearResults();
    resultsHead.style.display === "block"
    songs.forEach(song => appendToResults(song))
}
 
export function executesearch() {
    executesearchwithterm(document.getElementById("search").value)
}

function executesearchwithterm(searchterm) {
    clearResults();
    resultsHead.style.display === "block"
    console.log("Searching artists:" + searchterm)
    const result = search.search(searchterm)
    result.forEach(element => appendToResults(element.item))
}

export function random() {
    clearResults();
    resultsHead.style.display === "block"
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
    const results = document.getElementById('results');
    results.appendChild(newRow(newItem.artist, newItem.title, newItem.id));
}

function newRow(artist, song, id) {
    const tr = document.createElement('tr')
    const td1 = document.createElement('th')
    td1.appendChild(document.createTextNode(artist))
    const td2 = document.createElement('td')
    const a = document.createElement('a')
    a.setAttribute('href', 'https://youtu.be/' + id)
    a.setAttribute('target', '_blank')
    a.appendChild(document.createTextNode(song))
    td2.appendChild(a)
    tr.appendChild(td1)
    tr.appendChild(td2)
    return tr
}

function getRandomSong() {
    return songs[Math.floor(Math.random() * songs.length)]
}