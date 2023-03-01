/** @jsxImportSource @emotion/react */
function Bubble({ children, className, imageURL, onClick, ...props }) {
  const tint = 6;
  const mouseOverHandler = (event) => {
    console.log('Mouse over');
    event.target.style.backgroundColor = `rgba(0, 0, 50, 0.${tint})`;
    console.log(event.target.style.backgroundColor)
    event.target.addEventListener('mousedown', mouseDownHandler);
    event.target.addEventListener('mouseout', mouseOutHandler);
  }

  const mouseOutHandler = (event) => {
    console.log('Mouse out')
    console.log(tint - 2)
    event.target.style.backgroundColor = `rgba(0, 0, 50, 0.${tint - 2})`;
    event.target.removeEventListener('mousedown', mouseDownHandler); // I think this is just optimization? Possibly does nothing at all?
    event.target.removeEventListener('mouseout', mouseOutHandler); // I think this is just optimization? Possibly does nothing at all?
  }

  const mouseDownHandler = (event) => {
    event.target.style.backgroundColor = `rgba(0, 0, 50, 0.${tint + 2})`;
    event.target.addEventListener('mouseup', mouseUpHandler);
  }

  const mouseUpHandler = (event) => {
    event.target.style.backgroundColor = `rgba(0, 0, 50, 0.${tint})`;
    event.target.removeEventListener('mouseup', mouseUpHandler); // I think this is just optimization? Possibly does nothing at all?
  }

  return (
    <div 
    className={"Bubble"} 
    css={{
        width: '10vh',
        height: '10vh',
        border: '5px solid black',
        borderRadius: '50%',
        backgroundImage: `url(${imageURL})`,
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        backgroundPosition: 'center',
    }}
    >
      {children}
      <div 
        className="lens"
        css={{
            width: '100%',
            height: '100%',
            borderRadius: '50%',
            backgroundColor: 'rgba(0, 0, 50, 0.4)',
        }}
        onMouseOver={mouseOverHandler}
      onClick={onClick}
      >
      </div>
    </div>
  );
}

export default Bubble;