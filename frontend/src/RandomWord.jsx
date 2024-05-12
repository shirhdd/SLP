import React, {useEffect, useState} from 'react';
import Wheel from "./Wheel.jsx";

function RandomWord({setWord}) {

    return (
        <div>
            <Wheel setWord={setWord}/>
        </div>
    );
}

export default RandomWord;
