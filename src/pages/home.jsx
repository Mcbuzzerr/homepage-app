/** @jsxImportSource @emotion/react */
import React from "react";
import Bubble from "../components/bubble.jsx"
// import { redirect } from 'react-router-dom';
// import { useOutletContext } from 'react-router-dom';
// import { useLoaderData } from 'react-router-dom';
// import { Buffer } from 'buffer';

function Home() {
    const headerHeight = '11vh';
    const footerHeight = '11vh';
    const mainHeight = 'calc(100vh - ' + headerHeight + ' - ' + footerHeight + ')';

    const headerPadding = '1vh';
    const headerWidth = 'calc(100vw' + ' - ' + headerPadding + ' - ' + headerPadding + ')';
    const footerPadding = '1vh';
    const footerWidth = 'calc(100vw' + ' - ' + footerPadding + ' - ' + footerPadding + ')';

    const profileClickHandler = () => {
        console.log('Profile clicked');
        // add a window like div that has a profile switcher
    }

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            alignItems: 'center',
            height: '100vh',
            width: '100vw',
            position: 'absolute',
            top: '0',
            left: '0',
        }}>
            <header style={{
                height: headerHeight,
                width: headerWidth,
                padding: headerPadding,
                backgroundColor: '#69f',
            }}>
                {/* Profile */}
                <Bubble
                    onClick={profileClickHandler}
                    imageURL="https://cataas.com/cat?width=100&height=100"
                />
            </header>
            <main style={{
                height: mainHeight,
                width: '100vw',
                backgroundColor: '#58e'
            }}>

            </main>
            <footer style={{
                height: footerHeight,
                width: footerWidth,
                padding: footerPadding,
                backgroundColor: '#69f',
            }}>

            </footer>
        </div>
    )
}

export default Home;