// src/app/register/back_button.jsx

"use client";

const Button = ({ onClick, children }) => {
    return (
        <button onClick={onClick} className="btn btn-primary m-4 text-xl">
            {children}
        </button>
    );
};

export default Button;
