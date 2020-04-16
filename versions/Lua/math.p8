-- This code is part of Qiskit.
--
-- Copyright IBM 2020

-- Custom math table for compatibility with the Pico8

math = {}
math.pi = 3.14159
math.max = max
math.sqrt = sqrt
math.floor = flr
function math.random()
  return rnd(1)
end
function math.cos(theta)
  return cos(theta/(2*math.pi))
end
function math.sin(theta)
  return -sin(theta/(2*math.pi))
end
function math.randomseed(time)
end
os = {}

function quantumcircuit ()

  local qc = {}

  local function set_registers (n,m)
    qc._n = n
    qc._m = m or 0
  end
  qc.set_registers = set_registers

  qc.data = {}

  --Removable
  function qc.initialize (ket)
    ket_copy = {}
    for j, amp in pairs(ket) do
      if type(amp)=="number" then
        ket_copy[j] = {amp, 0}
      else
        ket_copy[j] = {amp[0], amp[1]}
      end
    end
    qc.data = {{'init',ket_copy}}
  end

  --Removable
  function qc.add_circuit (qc2)
    qc._n = math.max(qc._n,qc2._n)
    qc._m = math.max(qc._m,qc2._m)
    for g, gate in pairs(qc2.data) do
      qc.data[#qc.data+1] = ( gate )    
    end
  end

  function qc.rx (theta,q)
    qc.data[#qc.data+1] = ( {'rx',theta,q} )
  end

  --Removable: Note that qc.rz depends on this
  function qc.h (q)
    qc.data[#qc.data+1] = ( {'h',q} )
  end

  function qc.cx (s,t)
    qc.data[#qc.data+1] = ( {'cx',s,t} )
  end

  function qc.measure (q,b)
    qc.data[#qc.data+1] = ( {'m',q,b} )
  end

  --Removable: Note that qc.r depends on this
  function qc.rz (theta,q)
    qc.h(q)
    qc.rx(theta,q)
    qc.h(q)
  end
  
  --Removable
  function qc.ry (theta,q)
    qc.rx(math.pi/2,q)
    qc.rz(theta,q)
    qc.rx(-math.pi/2,q)
  end

  --Removable: Note that qc.z and qc.y depend on this
  function qc.x (q)
    qc.rx(math.pi,q)
  end

  --Removable
  function qc.z (q)
    qc.rz(math.pi,q)
  end

  --Removable
  function qc.y (q)
    qc.z(q)
    qc.x(q)
  end

  return qc

end


function simulate (qc, get, shots)

  if not shots then
    shots = 1024
  end

  function as_bits(num,bits)
    -- returns num converted to a bitstring of length bits
    -- adapted from https://stackoverflow.com/a/9080080/1225661
    local bitstring = {}
    for index = bits, 1, -1 do
        b = num - math.floor(num/2)*2
        num = math.floor((num - b) / 2)
        bitstring[index] = b
    end
    return bitstring
  end

  ket = {}
  for j=1,2^qc._n do
    ket[j] = {0,0}
  end
  ket[1] = {1,0}

  output_map = {}

  for g, gate in pairs(qc.data) do

    if gate[1]=='init' then

      for j, amp in pairs(gate[2]) do
          ket[j] = {amp[1], amp[2]}
      end

    elseif gate[1]=='m' then

      output_map[gate[3]] = gate[2]

    elseif gate[1]=="rx" or gate[1]=="h" then

      j = gate[#gate]

      for i0=0,2^j-1 do
        for i1=0,2^(qc._n-j-1)-1 do
          b1=i0+2^(j+1)*i1 + 1
          b2=b1+2^j

          e = {{ket[b1][1],ket[b1][2]},{ket[b2][1],ket[b2][2]}}

          if gate[1]=="rx" then
            theta = gate[2]
            ket[b1][1] = e[1][1]*math.cos(theta/2)+e[2][2]*math.sin(theta/2)
            ket[b1][2] = e[1][2]*math.cos(theta/2)-e[2][1]*math.sin(theta/2)
            ket[b2][1] = e[2][1]*math.cos(theta/2)+e[1][2]*math.sin(theta/2)
            ket[b2][2] = e[2][2]*math.cos(theta/2)-e[1][1]*math.sin(theta/2)
          elseif gate[1]=="h" then
            for k=1,2 do
              ket[b1][k] = (e[1][k] + e[2][k])/math.sqrt(2)
              ket[b2][k] = (e[1][k] - e[2][k])/math.sqrt(2)
            end
          end

        end
      end

    elseif gate[1]=="cx" then

      s = gate[2]
      t = gate[3]

      if s>t then
        h = s
        l = t
      else
        h = t
        l = s
      end

      for i0=0,2^l-1 do
        for i1=0,2^(h-l-1)-1 do
          for i2=0,2^(qc._n-h-1)-1 do
            b1 = i0 + 2^(l+1)*i1 + 2^(h+1)*i2 + 2^s + 1
            b2 = b1 + 2^t
            e = {{ket[b1][1],ket[b1][2]},{ket[b2][1],ket[b2][2]}}
            ket[b1] = e[2]
            ket[b2] = e[1]
          end
        end
      end

    end

  end


  if get=="statevector" then
    return ket

    --Removable: if memory and/or counts not needed
    --code required for memory and counts begins here
    --the above `if` statement would need to be ended
  else

    probs = {}
    for j,amp in pairs(ket) do
      probs[j] = amp[1]^2 + amp[2]^2
    end

    m = {}
    for s=1,shots do
      cumu = 0
      un = true
      r = math.random()
      for j,p in pairs(probs) do
        cumu = cumu + p
        if r<cumu and un then
          raw_out = as_bits(j-1,qc._n)
          out = ""
          for b=0,qc._m-1 do
            if output_map[b] then
              out = raw_out[qc._n-output_map[b]]..out
            end
          end
          m[s] = out
          un = false
        end
      end
    end

    if get=="memory" then
      return m
    end

    --code required for memory ends here

    if get=="counts" then
      c = {}
      for s=1,shots do
        if c[m[s]] then
          c[m[s]] += 1
        else
          if m[s] then
            c[m[s]] = 1
          else
            -- what's this all about?
            if c["error"] then
              c["error"] += 1 
            else
              c["error"] = 1 
            end
          end
        end
      end
      return c
    end

  end
   --code required for counts ends here

end