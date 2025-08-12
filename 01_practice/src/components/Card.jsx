import React from 'react'

const Card = ({length,setLength,number,setNumber, password, chars, setChars,passRef,copyPassToClipBoard}) => {


  return (
   <>
   <div className='text-2xl m-4 p-4 text-center text-amber-950' >
    <div>
    <h1>Password Generator</h1>  
    <input type="text" 
      value={password}
      placeholder='HELLOWORLD'
      readOnly
      ref={passRef}
    />
     <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={copyPassToClipBoard}>
  Click
</button>
</div>

   
   <input type="range" min="0" max="20" value={length} className='cursor-pointer' onChange={(e)=>{
    setLength(e.target.value)
   }}/> <label>Length({length})</label>
  
    <h2>Pass Len : {length}</h2> 
  <p>Include Number : <input type="checkbox" value={number} conchange={() => {
      setNumber((prev) =>{ !prev}
       
      )
    
  }} className="peer h-5 w-5 cursor-pointer transition-all appearance-none rounded shadow hover:shadow-md border border-slate-300 checked:bg-green-600 checked:border-green-600-600" id="check1" /></p>
  <p>Include special Chars : <input type="checkbox" className="peer h-5 w-5 cursor-pointer transition-all appearance-none rounded shadow hover:shadow-md border border-slate-300 checked:bg-green-600 checked:border-green-600-600" id="check2" value={chars} onChange={()=>
    {
      setChars((prev) =>{ !prev})
    }
  } /></p>

    <h2>Pass:  {password}</h2> 

   </div>
      
   </>
  )
}

export default Card
