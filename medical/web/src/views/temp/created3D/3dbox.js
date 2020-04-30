class ElfCube {
  constructor(props = {}) {
    this.cubeEle = null
    this.cubeInner = null
    this.cubeW = null
    this.cubeH = 200
    this.axisX = 0
    this.axisY = 0
  }

  componentDodMount() {
    // 实例，初始化执行的方法
    this.cubeEle = document.querySelector('.cube')
    this.cubeInner = this.cubeEle.querySelector('.cube-inner')
    this.cubeW = this.cubeEle.offsetWidth
    this.cubeH = this.cubeEle.offsetHeight
    // this.run()
    return this
  }

  run() {
    this.cubeEle.addEventListener('mouseover', (e) => this.hoverOut(e), false)
    this.cubeEle.addEventListener('mousemove', (e) => this.move(e), false)
    this.cubeEle.addEventListener('mouseout', (e) => this.hoverOut(e), false)
  }

  getAxisX(e) {
    const left = this.cubeEle.offsetLeft
    return (
      e.pageX -
      left -
      (this.cubeW / 2) * (this.cubeW > this.cubeH ? this.cubeH / this.cubeW : 1)
    )
  }

  getAxisY(e) {
    const top = this.cubeEle.offsetTop
    return (
      e.pageY -
      top -
      (this.cubeH / 2) * (this.cubeH > this.cubeW ? this.cubeW / this.cubeH : 1)
    )
  }

  hoverOut(e) {
    // 进入/离开
    e.preventDefault()
    this.axisX = this.getAxisX(e)
    this.axisY = this.getAxisY(e)
    if (e.type == 'mouseout') {
      // 离开
      this.axisX = 0
      this.axisY = 0
      console.log('离开')
      this.cubeInner.className = 'cube-inner running'
    } else {
      this.cubeInner.className = 'cube-inner'
      console.log('进入')
    }
    const rotate = `rotateX(${-this.axisY}deg) rotateY(${-this.axisX}deg)`
    this.cubeInner.style.WebkitTransform = this.cubeInner.style.transform = rotate
  }

  move(e) {
    e.preventDefault()
    this.axisX = this.getAxisX(e)
    this.axisY = this.getAxisY(e)
    const rotate = `rotateX(${-this.axisY}deg) rotateY(${-this.axisX}deg)`
    this.cubeInner.style.WebkitTransform = this.cubeInner.style.transform = rotate
  }
}
const ElfCubes = new ElfCube()
// ElfCubes.componentDodMount()

export default ElfCubes
