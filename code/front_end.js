const userCardTemplate = document.querySelector('[data-user-template]')
const userCardContainer = document.querySelector('[data-user-cards-container]')
const submitMessage = document.querySelector('.submit-message')
const likerScale = document.querySelector('.wrap')

const searchButton = document.getElementById('search_btn')
const submitButton = document.getElementById('likert_btn')
const addButton = document.getElementById('add_btn')
var d3frame = document.getElementById('image-frame')

function reloadD3Graph(searchContent) {
    d3frame.contentWindow.postMessage(
        {
            call: 'reloadD3Graph',
            value: { searchContent: searchContent },
        },
        '*'
    )
}
function getSearchResult(searchContent) {
    fetch('http://127.0.0.1:5000/recommend/' + searchContent)
        .then((res) => res.json())
        .then((data) => {
            console.log(data)
            if (data == null) {
                addButton.classList.add('hide')
                userCardContainer.innerHTML = ''
            } else if (data.children.length == 0) {
                addButton.classList.add('hide')
                userCardContainer.innerHTML = ''
            } else {
                const checkboxContainer = document.querySelectorAll('.checkbox-container')
                checkboxContainer.forEach((checkbox) => {
                    checkbox.classList.remove('hide')
                })
                userCardContainer.innerHTML = ''
                music = data.children.map((music) => {
                    const card = userCardTemplate.content.cloneNode(true).children[0]
                    const header = card.querySelector('[data-header]')
                    header.textContent = music.name
                    userCardContainer.append(card)
                })
            }
        })
}

// Searching for music
searchButton.addEventListener('click', () => {
    const musicList = document.querySelector('.show-container')
    const coverImage = document.querySelector('.cover-image')

    // hide the cover image
    coverImage.classList.add('hide')
    //data input: search content
    const searchContent = document.getElementById('searchBar').value

    musicList.classList.remove('hide')
    submitMessage.classList.add('hide')
    addButton.classList.remove('hide')
    likerScale.classList.remove('hide')

    var r = document.getElementsByClassName("image-space")
    console.log(r)

    //search the recommend list
    getSearchResult(searchContent);
    reloadD3Graph(searchContent)
    document.getElementById('list-title').textContent = 'Music Recommendation List (Top 5)'
})

// Add the interest result in to DB
addButton.addEventListener('click', () => {
    const checkBoxes = document.querySelectorAll('#myCheck')
    console.log(checkBoxes)
    let count = 0
    let total = 0
    checkBoxes.forEach((checkBox) => {
        if (checkBox.checked == true) {
            count += 1
        }
        total += 1
    })
    var feedback;
    if (total == 0) {
        feedback = 0;
    } else {
        feedback = Number.parseFloat(count / total).toFixed(2);
    }

    fetch(
        'http://127.0.0.1:5000/feedback/music_feedback/' + feedback).then((res) => {
        console.log(res.json())
    })

    // hide all the checkbox after ADD complete
    const checkboxContainer = document.querySelectorAll('.checkbox-container')
    checkboxContainer.forEach((checkbox) => {
        checkbox.classList.add('hide')
    })

    // hide the add button
    addButton.classList.add('hide')

    // show the complete message
    submitMessage.classList.remove('hide')
})

// Add the user feedback in to DB
submitButton.addEventListener('click', () => {
    likerScale.classList.add('hide')
    const rd1 = document.getElementById('rd1').checked
    const rd2 = document.getElementById('rd2').checked
    const rd3 = document.getElementById('rd3').checked
    const rd4 = document.getElementById('rd4').checked
    const rd5 = document.getElementById('rd5').checked

    let score = 0
    if (rd5) score = 5
    else if (rd4) score = 4
    else if (rd3) score = 3
    else if (rd2) score = 2
    else score = 1
    console.log(score)
    fetch('http://127.0.0.1:5000/feedback/user_feedback/' + score).then(
        (res) => {
            console.log(res.json())
        }
    )
})