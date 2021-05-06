let doc = document
const theDate = doc.getElementById('theDate')
const theTime = doc.getElementById('theTime')

function currentTime() {
    let date = new Date();
    const DateOptions = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    };
    const TimeOptions = {
        hour12: false,
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    };

    theTime.innerHTML = date.toLocaleTimeString([], TimeOptions);
    theDate.innerHTML = date.toLocaleDateString([], DateOptions);

    let t = setTimeout(function () {
        currentTime()
    }, 1000); /* setting timer */

}

currentTime(); /* calling currentTime() function to initiate the process */

