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
}
const ElfCubes = new ElfCube()
// ElfCubes.componentDodMount()

export default ElfCubes
