import { useState } from 'react'
import axios from "axios"

function ApplyPage() {
  const [complexId, setComplexId] = useState("")
  const [searched, setSearched] = useState(false)
  const [complexInfo, setComplexInfo] = useState({})


  return (
    <>
    <div>
      <h2>단지 등록 페이지</h2>
    </div>
    <div style={{display: "flex", flexDirection: "column"}}>
      <label>단지 등록</label>
      <input value={complexId} onChange={(event) => {
        setComplexId(event.target.value)
      }}></input>
      <div>
        <button onClick={async (event) => {
          console.log(complexId)
          const response = await axios.post("http://localhost:8000/complex_search", {
            complexId: complexId
          })

          if (response.status === 200) {
            setComplexInfo(response.data[complexId])
          }

          setSearched(true)

        }}>검색</button>

      <div>
        <div>
        <label>단지명</label>
        <span>{complexInfo?.complex_name || ""}</span>
        </div>
        <div>
          <label>세대수</label>
          <span>{complexInfo?.complex_num || ""}</span>
        </div>
        <div>
          <label>건설사</label>
          <span>{complexInfo?.complex_company || ""}</span>
        </div>
        <div>
          <label>주소</label>
          <span>{complexInfo?.complex_addr || ""}</span>
        </div>
        <div>
          <label>세대평수</label>
          <span>{complexInfo?.complex_width?.join(", ")  || ""}</span>
        </div>
      </div>
        <div>
      <button disabled={!searched} onClick={async (event) => {
        console.log(complexInfo)

        const response = await axios.post("http://localhost:8000/complex_apply", complexInfo)

        console.log(response)
        
      }}>등록</button>
      </div>
      </div>
    </div>


    </>
  )
}

export default ApplyPage
