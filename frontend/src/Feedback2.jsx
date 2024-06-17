import React from 'react';
import styled, { keyframes, css } from 'styled-components';
import { useSpring, animated } from 'react-spring';
import { FaSmile, FaFrown, FaClock } from 'react-icons/fa';

const fadeIn = keyframes`
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
`;

const flip = keyframes`
    0% {
        transform: rotateY(0deg);
    }
    100% {
        transform: rotateY(360deg);
    }
`;

const FeedbackContainer = styled(animated.div)`
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    margin: 20px auto;
    border-radius: 10px;
    width: 50%;
    background-color: ${props => {
        if (props.isGood) return '#d4edda';
        if (props.isBad) return '#f8d7da';
        return '#fff3cd';
    }};
    color: ${props => {
        if (props.isGood) return '#155724';
        if (props.isBad) return '#721c24';
        return '#856404';
    }};
    border: 1px solid ${props => {
        if (props.isGood) return '#c3e6cb';
        if (props.isBad) return '#f5c6cb';
        return '#ffeeba';
    }};
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    animation: ${fadeIn} 1s ease-in;
`;

const Emoji = styled.div`
    font-size: 2em;
    margin-right: 10px;
    ${props => props.isGood && css`
        animation: ${flip} 2s infinite;
    `}
`;

const FeedbackText = styled.div`
    font-size: 1.2em;
`;

const Bounce = styled.div`
    display: inline-block;
    ${props => props.isGood && css`
        animation: bounce 2s infinite;
    `}
    @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-30px);
    }
    60% {
        transform: translateY(-15px);
    }
}
`;

const Feedback2 = ({ text, status }) => {
    const animationProps = useSpring({
        opacity: 1,
        transform: 'translateY(0)',
        from: { opacity: 0, transform: 'translateY(-20px)' },
    });

    const isGood = status === 'good';
    const isBad = status === 'bad';
    const isWaiting = status === 'waiting';

    return (
        <FeedbackContainer style={animationProps} isGood={isGood} isBad={isBad} isWaiting={isWaiting}>
            <Emoji isGood={isGood}>
                {isGood ? <FaSmile /> : isBad ? <FaFrown /> : <FaClock />}
            </Emoji>
            <FeedbackText>
                <Bounce isGood={isGood}>{text}</Bounce>
            </FeedbackText>
        </FeedbackContainer>
    );
};

export default Feedback2;
