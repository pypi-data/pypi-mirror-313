console.log('[{{version}}] Executing {{script_name}} at {{date_now}}')


var points = [];
var dbInstance

let capturing = false;  // Flag to control capturing

// Function to open and initialize the IndexedDB
function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('MouseMovementsDB', 1);

        request.onupgradeneeded = function(event) {
            let db = event.target.result;
            db.createObjectStore('points', { autoIncrement: true });
        };

        request.onsuccess = function(event) {
            resolve(event.target.result);
        };

        request.onerror = function(event) {
            reject('Database error: ' + event.target.errorCode);
        };
    });
}

// Function to store points in IndexedDB
function storePoints(db, point) {
    const transaction = db.transaction(['points'], 'readwrite');
    const store = transaction.objectStore('points');
    store.add({ time: Date.now(), coords: point });
}

// Function to handle mouse movements
function handleMouseMove(event) {
    point  = { x: event.pageX, y: event.pageY }
    console.log('storing', point)
    storePoints(dbInstance, point);
}

function set_db_capture() {
    // Setup DB and event listeners
    openDB().then(db => {
        dbInstance = db;  // Save the db instance for later use
        document.addEventListener('mousemove', handleMouseMove);
        console.log('DB initialized and ready to capture mouse movements.');
    });
}

function replay_from_db() {
    let mousePointer = document.getElementById('mouse_pointer');
    if (!mousePointer) {
        // Create and style the mouse pointer if it doesn't exist
        mousePointer = document.createElement('i');
        mousePointer.id = 'mouse_pointer';
        mousePointer.className = 'fa fa-mouse-pointer'; // FontAwesome icon class
        mousePointer.style.position = 'absolute';
        mousePointer.style.fontSize = '24px'; // Size of the icon
        document.body.appendChild(mousePointer);
    }

    // Open the existing database
    const request = indexedDB.open('MouseMovementsDB', 1);

    request.onsuccess = function(event) {
        const db = event.target.result;
        const transaction = db.transaction(['points'], 'readonly');
        const store = transaction.objectStore('points');
        const cursorRequest = store.openCursor();

        let points = [];


       cursorRequest.onsuccess = function(e) {
            const cursor = e.target.result;
            if (cursor) {
                points.push(cursor.value.coords); // Add the point to the array
                cursor.continue(); // Continue to the next record
            } else {
                // No more entries
                animateMouseMovements(points, 10);
            }
        };

        cursorRequest.onerror = function(e) {
            reject('Cursor request failed');
        };
    };

    request.onerror = function(event) {
        console.error('Database error: ' + event.target.errorCode);
    };
}


//// -----

function create_target_div() {
    remove_mouse_icon()
    var newTextarea = $('<textarea id="new_div"></textarea>');

    // Apply CSS styles to the new textarea
    newTextarea.css({
        'width': '630px',
        'height': '250px',
        'background-color': 'azure',
        'resize': 'none'  // Prevent the textarea from being resizable
    });

    // Replace any existing content in #dev-area with the new textarea
    $('#dev-area').html(newTextarea);

}

function attach_mouse_handler() {
    console.log('enabling mouse capture')
    let logArea = $('#new_div');

    // Function to update textarea with mouse coordinates
    function updateCoordinates(event) {
        var x = event.pageX;
        var y = event.pageY;
        points.push({ x: x, y: y });
        // Append the new coordinates to the textarea content
        logArea.val(logArea.val() + 'X: ' + x + ', Y: ' + y + '\n');

        // Optionally, scroll to the bottom of the textarea to keep the latest entry in view
        logArea.scrollTop(logArea[0].scrollHeight);
    }

    // Remove any existing mousemove handlers to prevent duplicates
    disable_mouse_handler()

    // Attach new mousemove event to the document
    $(document).mousemove(updateCoordinates);
}

function disable_mouse_handler() {
    console.log('disabling mouse capture')
    $(document).off('mousemove');
}

// function simulate_mouse_move(startX, startY, endX, endY, steps) {
//     // Function to create and dispatch a mouse event
//     function dispatchMouseEvent(x, y) {
//         var event = new MouseEvent('mousemove', {
//             bubbles: true,
//             cancelable: true,
//             view: window,
//             clientX: x,
//             clientY: y
//         });
//         document.dispatchEvent(event);
//     }
//
//     // Calculate intermediate steps
//     for (let i = 0; i <= steps; i++) {
//         let t = i / steps;
//         let currentX = startX + (endX - startX) * t;
//         let currentY = startY + (endY - startY) * t;
//         dispatchMouseEvent(currentX, currentY);
//     }
// }

function remove_mouse_icon() {
    var mousePointer = document.getElementById('mouse_pointer');

    if (mousePointer) {
        mousePointer.remove()
    }
}
function animateMouseMovements(points, interval) {

    var mousePointer = document.getElementById('mouse_pointer');

    if (!mousePointer) {
        mousePointer = document.createElement('i',);
        mousePointer.id = 'mouse_pointer'
        mousePointer.className = 'fa fa-mouse-pointer'; // Use the appropriate FontAwesome class
        mousePointer.style.position = 'absolute';
        mousePointer.style.fontSize = '24px'; // Set the size of the icon
        document.body.appendChild(mousePointer);
    }

    let index = 0;

    function moveToNextPoint() {
        if (index < points.length) {
            const point = points[index++];
            console.log(point)
            mousePointer.style.left = point.x + 'px';
            mousePointer.style.top = point.y + 'px';
            setTimeout(moveToNextPoint, interval);
        }
        else {
            remove_mouse_icon()
        }
    }

    moveToNextPoint();
}

function add_start_capture() {
     // Create a Bootstrap 5 button dynamically
    var button = document.createElement('button');
    button.className     = 'btn btn-primary'; // Bootstrap 5 button class
    button.textContent   = 'Start Capturing mouse';
    button.style.margin  = '10px'
    button.onclick       = attach_mouse_handler

    document.getElementById('dev-area').appendChild(button)
}

function add_replay_button() {
     // Create a Bootstrap 5 button dynamically
    var replayButton = document.createElement('button');
    replayButton.className = 'btn btn-primary'; // Bootstrap 5 button class
    replayButton.textContent = 'Replay Movements';
    replayButton.style.margin  = '10px'
    replayButton.onclick = function() {
        disable_mouse_handler()
        animateMouseMovements(points, 10); // Attach replay function to button click
    };
    document.getElementById('dev-area').appendChild(replayButton)
}

function add_replay_from_db_button() {
     // Create a Bootstrap 5 button dynamically
    var replayButton = document.createElement('button');
    replayButton.className = 'btn btn-primary'; // Bootstrap 5 button class
    replayButton.textContent = 'Replay from DB';
    replayButton.style.margin  = '10px'
    replayButton.onclick = replay_from_db
    document.getElementById('dev-area').appendChild(replayButton)
}


// Usage: Animate with a 100ms interval between points


create_target_div()
add_start_capture()
add_replay_button()
add_replay_from_db_button()
replay_from_db()
//set_db_capture()

//simulate_mouse_move(100, 100, 400, 400, 10);
//disable_mouse_handler()
//animateMouseMovements(points, 100);



//
//
// disable_mouse_handler()

