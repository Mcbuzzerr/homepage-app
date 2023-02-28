/** @jsxImportSource @emotion/react */

function Window({className, doXButton, width, height, ...props}) {
    return (
        <div 
            className="window"
            css={{
                width: width,
                height: height,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                alignItems: 'center',
                backgroundColor: '#47d',
            }}
        >
            <div
                className="navBar"
            >
                {/* X Button Component */}
            </div>

        </div>
    )
}

export default Window;