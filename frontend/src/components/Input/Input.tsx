import React from "react"
import { InputProps } from "./Input.types"

const Input: React.FC<InputProps> = ({ className, value, onChange, ...rest }) => {
	return (
		<input className={[className, 'border-black border-3 w-full hover:bg-gray-300/50'].join(" ")} value={value} onChange={onChange} {...rest} />
	)
}

export default Input;
