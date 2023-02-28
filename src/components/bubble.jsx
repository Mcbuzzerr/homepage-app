/** @jsxImportSource @emotion/react */
function Bubble({ children, className, imageURL, onClick, ...props }) {
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
    
    {...props}>
      {children}
      <div 
        className="lens"
        css={{
            width: '100%',
            height: '100%',
            borderRadius: '50%',
            backgroundColor: 'rgba(0, 0, 50, 0.4)',
        }}
        onMouseOver={(event) => {
          const tint = 0.6;
          console.log('Mouse over');
          event.target.style.backgroundColor = `rgba(0, 0, 50, ${tint})`;
          event.target.addEventListener('mousedown', () => {
              event.target.style.backgroundColor = `rgba(0, 0, 50, ${tint + 0.2})`;
              event.target.addEventListener('mouseup', () => {
                  event.target.style.backgroundColor = `rgba(0, 0, 50, ${tint})`;
                  event.target.removeEventListener('mouseup', () => {}); // I think this is just optimization? Possibly does nothing at all?
              });
          });
          event.target.addEventListener('mouseout', () => {
              event.target.style.backgroundColor = `rgba(0, 0, 50, ${tint - 0.2}})`;
              event.target.removeEventListener('mouseout', () => {}); // I think this is just optimization? Possibly does nothing at all?
              event.target.removeEventListener('mousedown', () => {}); // I think this is just optimization? Possibly does nothing at all?
          });
      }}
      onClick={onClick}
      >
      </div>
    </div>
  );
}

export default Bubble;