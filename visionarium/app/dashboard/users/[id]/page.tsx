const page = ({params} : {params:{id: string}}) => {
    const {id} = params;
  return (
    <div>
      <h2 className="text-3xl">User ID:  {id}</h2>
    </div>
  )
}

export default page
