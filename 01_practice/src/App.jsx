import { useState,useCallback,useEffect,useRef} from 'react'
import Card from './components/Card'

function App() {
  const [length, setLength] = useState(8)
  const [number, setNumber] = useState(false)
  const [chars, setChars] = useState(false)
  const [password, setPassword] = useState('')

  const passRef = useRef(null)

const copyPassToClipBoard = useCallback(() => {
  passRef.current?.select() 
  window.navigator.clipboard.writeText(password)
},[password]
)
const passwordGenerator = useCallback(()=>{
  let pass = ""
  let str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  if (number) str += "0123456789"
  if (chars) str += "!@#$%^&*()_+~`|}{"

  for (let i = 0; i < length; i++) {
   let char =Math.floor( Math.random()* str.length)
   pass += str.charAt(char)
    
  }
  setPassword(pass)
  console.log(password)
}, [length,number,chars,setPassword])

useEffect(()=> {
  passwordGenerator()
},[length,number,chars,passwordGenerator])

  return (
    <>
    <Card length={length} setLength={setLength} number={number} setNumber={setNumber} password={password} chars = {chars} setChars ={setChars} passRef={passRef} copyPassToClipBoard={copyPassToClipBoard} />
    </>
  )
}

export default App
