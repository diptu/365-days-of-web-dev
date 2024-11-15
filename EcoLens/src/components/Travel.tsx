import React, {useState} from 'react'
type InputEvent = React.ChangeEvent<HTMLInputElement>;
type formEvent = React.FormEvent<HTMLFormElement>;


type Travel = {
    title : string
}
const Travel = (props: Travel) => {

  const [trvel, setTravel] = useState({
    flight: "",
    public_transit: "",
    company_gasoline_car_driven : "",
    company_diesel_car_driven: "",
  });


  const Update = (e:InputEvent) => {
    setTravel({ ...trvel, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e:formEvent) => {
    console.log(trvel);
    e.preventDefault();
  };
  return (
    <div className='flex gap-4 mb-4'>
        <h2>{props.title}</h2>
      <form action="#" onSubmit={handleSubmit}>
        <div>
          <input type="number" required name="flight" min="0"  step="any" placeholder='km flown per year' onChange={Update} />
        </div>
      
        <div className='flex gap-4 mb-4'>
          <input type="number" required name="public_transit" min="0"  step="any" placeholder='km per year' onChange={Update} />
       </div>

       <div className='flex gap-4 mb-4'>
          <input type="number" required name="company_gasoline_car_driven" min="0"  step="any" placeholder='Company Gasoline - km driven per year' onChange={Update} />
       </div>

       <div className='flex gap-4 mb-4'>
          <input type="number" required name="company_diesel_car_driven" min="0"  step="any" placeholder='Company diesel - km driven per year' onChange={Update} />
       </div>
       <div className='flex gap-4 mb-4'>
           <input type="submit" value="update" />
        </div>
      </form>
    </div>
  )
}

export default Travel
