import Link from "next/link"

const page = () => {
  return (
    <div>
      <h2>User Details</h2>
      <li><Link href="users/1">user-1</Link></li>
      <li><Link href="users/2">user-2</Link></li>
      <li><Link href="users/3">user-3</Link></li>

    </div>
  )
}

export default page
