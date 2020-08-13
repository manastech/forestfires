function shuffle(array) {
	var currentIndex = array.length, temporaryValue, randomIndex;
  
	// While there remain elements to shuffle...
	while (0 !== currentIndex) {
  
	  // Pick a remaining element...
	  randomIndex = Math.floor(Math.random() * currentIndex);
	  currentIndex -= 1;
  
	  // And swap it with the current element.
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
			fire: {
				x: 850,
				y: 850
			}
		},
		background = {
			width: window.innerWidth,
			height: window.innerHeight,
			position: {},
			size: {}
		},
		frame = {
			width: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-width')),
			height: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-height')),
			x: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-x')),
			y: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-y')),
			center: {
				x: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-x')) + parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-width')) / 2,
				y: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-y')) + parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fire-boundary-frame-height')) / 2
			},
			position: {}
		},
		scale = Math.max(
			frame.center.x / picture.fire.x,
			frame.center.y / picture.fire.y,
			(background.width - frame.center.x) / (picture.width - picture.fire.x),
			(background.height - frame.center.y) / (picture.height - picture.fire.y)
		)

	background.size.width = Math.round(picture.width * scale)
	background.size.height = Math.round(picture.height * scale)
	background.position.x = Math.round(frame.center.x - picture.fire.x * scale)
	background.position.y = Math.round(frame.center.y - picture.fire.y * scale)

	frame.position.x = Math.round(background.position.x - frame.center.x + frame.width / 2)
	frame.position.y = Math.round(background.position.y - frame.center.y + frame.height / 2)

	style.setProperty('--fire-boundary-size', `${background.size.width}px ${background.size.height}px`)
	style.setProperty('--fire-boundary-background-position', `${background.position.x}px ${background.position.y}px`)
	style.setProperty('--fire-boundary-frame-position', `${frame.position.x}px ${frame.position.y}px`)
}

window.onload = handleLoad
window.onresize = handleResize