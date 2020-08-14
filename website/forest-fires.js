function shuffle(array) {
	var currentIndex = array.length, temporaryValue, randomIndex;
	while (0 !== currentIndex) {
	  randomIndex = Math.floor(Math.random() * currentIndex);
	  currentIndex -= 1;
	  temporaryValue = array[currentIndex];
	  array[currentIndex] = array[randomIndex];
	  array[randomIndex] = temporaryValue;
	}
	return array;
}

function handleLoad() {
	const animals = shuffle(Array.from(document.querySelectorAll('.animal')).filter(animal => window.getComputedStyle(animal).display !== 'none'))
	animals.slice(0, Math.round(animals.length * 0.75)).forEach(animal => {
		animal.classList.add('disabled')
	})
	handleResize()
}

function handleResize() {
	let style = document.documentElement.style,
		picture = {
			width: 2800,
			height: 1800,
		},
		fire = {
			x: 660,
			y: 680,
			width: 350,
			height: 350
		},
		background = {
			width: window.innerWidth,
			height: window.innerHeight,
		},
		frame = {
			x: document.querySelector('#mask').offsetLeft,
			y: document.querySelector('#mask').offsetTop,
			width: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-width')),
			height: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-height'))
		},
		scale = Math.max(
			background.width / picture.width,
			background.height / picture.height,
			frame.x / fire.x,
			frame.y / fire.y,
			(frame.x + frame.width / 2) / (fire.x + fire.width / 2),
			(frame.y + frame.height / 2) / (fire.y + fire.height / 2),
			(background.width - frame.width - frame.x) / (picture.width - fire.width - fire.x),
			(background.height - frame.height - frame.y) / (picture.height - fire.height - fire.y),
			(background.width - frame.width / 2 - frame.x) / (picture.width - fire.width / 2 - fire.x),
			(background.height - frame.height / 2 - frame.y) / (picture.height - fire.height / 2 - fire.y)
		)
	console.log(frame, scale)
	document.querySelector('#value').textContent = scale.toFixed(3)
	style.setProperty('--fire-boundary-size', `${picture.width * scale}px ${picture.height * scale}px`)
	style.setProperty('--fire-boundary-background-position', `${(frame.x + frame.width / 2) - (fire.x + fire.width / 2) * scale}px ${(frame.y + frame.height / 2) - (fire.y + fire.height / 2) * scale}px`)
	style.setProperty('--fire-boundary-frame-position', `${frame.width / 2 - (fire.x + fire.width / 2) * scale}px ${frame.height / 2 - (fire.y + fire.height / 2) * scale}px`)
}

window.onload = handleLoad
window.onresize = handleResize