program moVecAngle

IMPLICIT NONE
logical :: exists
integer :: nmo,ncoef,stat,i,j,k,NR,ios,nclines,getc,modformat,cpermo,nargs
integer :: mo1,mo2
integer :: ii,jj
real*8  :: angleij,t1,t2
integer, parameter :: maxrecs = 100000000
character(150) :: line,title
character(16*5) :: xline
character(1) :: junk
character(150), dimension(:), allocatable :: args
real*8 :: pi,sumsqA,sumsqB,EPS
real*8, allocatable :: angles(:,:)
real*8, allocatable :: vecA(:),tempA(:),normA(:),normB(:)
real*8, allocatable :: vecB(:),tempB(:)
real*8, allocatable :: matA(:,:),matB(:,:),matAT(:,:),matBT(:,:)
real*8, allocatable :: magA(:),magB(:)
real*8, dimension(5) :: cline
real*8, allocatable  :: modcline(:)
real*8, allocatable :: dotAB(:,:),magAB(:,:),quotAB(:)

CALL CPU_TIME(t1)

! defines pi and number correction 
pi=4.0*ATAN(1.0)
EPS=1d-30

! arguments are the files by which mos compared
write(*,*) "Parsing arguments..."
nargs=IARGC()
ALLOCATE(args(nargs))
DO i=1,nargs
  CALL GETARG(i,args(i))
ENDDO
IF (nargs.eq.4) THEN
  READ(args(3),*) mo1
  READ(args(4),*) mo2
ENDIF

! If program has been run before, than angles.dat exists and can just be read
INQUIRE(FILE='angles.dat',exist=exists)
IF (exists) THEN
  write(*,*) "Angles.dat exists!"
  write(*,*) "  Parsing old angles.dat for desired angle"
  NR=0
  OPEN(UNIT=24,FILE='angles.dat',status='old')
  REWIND(24)
  DO i=1,maxrecs
    READ(24,*,IOSTAT=ios) junk
    IF (ios /= 0) EXIT
    IF (i ==maxrecs) THEN
      write(*,*) "Error:  Maximum number of records exceeded..."
      write(*,*) "Exiting program now..."
      STOP
    ENDIF
    NR=NR+1
  ENDDO
  REWIND(24)
  DO i=1,NR
    READ(24,FMT=33) ii,jj,angleij
!    IF (ii==mo1.and.jj==mo2) THEN
!      write(*,*) " mo1  mo2    angle"
!      write(*,FMT=33)ii,jj,angleij
!      STOP
!    ENDIF
    IF (ii==jj) THEN
!      write(*,*) " mo1  mo2    angle"
      write(*,FMT=33)ii,jj,angleij
    ENDIF
  ENDDO
ELSE

write(*,*) "  MO-1   :: ",mo1
write(*,*) "  MO-2   :: ",mo2
write(*,*) "  File-1 :: ",args(1)
write(*,*) "  File-2 :: ",args(2)

write(*,*) "Acquiring MO vectors in ",TRIM(ADJUSTL(args(1)))
!determines the number of lines in the file
NR=0
OPEN(UNIT=1,FILE=args(1))
DO i=1,maxrecs
  READ(1,*,IOSTAT=ios) junk
  IF (ios /= 0) EXIT
  IF (i == maxrecs) THEN
    write(*,*) "Error:  Maximum number of records exceeded..."
    write(*,*) "Exiting program now..."
    STOP
  ENDIF
  NR = NR + 1
ENDDO
REWIND(1)
write(*,*)  "  Number of lines in ",TRIM(ADJUSTL(args(1)))," = ",NR

! defines the number of molecular orbitals and coefficients within a file
DO i=1,NR
  READ(1, '(A)',IOSTAT=ios) line
  IF (line(1:23)=="Alpha Orbital Energies") THEN
    READ(line,FMT=30)title,nmo
    write(*,*) "  number of orbitals = ",nmo
  ENDIF
  IF (line(1:22)=="Alpha MO coefficients") THEN
    READ(line,FMT=30)title,ncoef
    write(*,*) "  number of coefficients = ",ncoef
  ENDIF
ENDDO
REWIND(1)

! defines number of lines required to print coefficients
IF (MOD(ncoef,5)>0) THEN
  nclines=(ncoef/5)+1
ELSE
  nclines=(ncoef/5)
ENDIF
write(*,*) "  number of lines to print coefficients = ",nclines

! allocates the size of vecA
ALLOCATE(vecA((ncoef/nmo)*(ncoef/nmo)))
ALLOCATE(modcline(MOD(ncoef,5)))

xline(1:len(xline))=REPEAT('X',(16*5))

! grabs coefficient vectors for file A
DO i=1,NR
  READ(1, '(A)',IOSTAT=ios) line
  IF (line(1:22)=="Alpha MO coefficients") then
    DO j=1,nclines
      READ(1, '(A)',IOSTAT=ios) xline
      IF (j<nclines) THEN
        DO k=1,5
          READ(xline(((k-1)*16)+1:k*16),FMT=1) vecA(((j-1)*5)+k)
        ENDDO
      ELSEIF (j==nclines) THEN
        DO k=1,MOD(ncoef,5)
          READ(xline(((k-1)*16)+1:k*16),FMT=1) vecA(((j-1)*5)+k)
        ENDDO
      ENDIF
    ENDDO
  EXIT
  ENDIF
ENDDO
close(1)

write(*,*) "Acquiring MO vectors in ",TRIM(ADJUSTL(args(2)))

!determines the number of lines in the file
NR=0
OPEN(UNIT=1,FILE=args(2))
DO i=1,maxrecs
  READ(1,*,IOSTAT=ios) junk
  IF (ios /= 0) EXIT
  IF (i == maxrecs) THEN
    write(*,*) "Error:  Maximum number of records exceeded..."
    write(*,*) "Exiting program now..."
    STOP
  ENDIF
  NR = NR + 1
ENDDO
REWIND(1)
write(*,*)  "  Number of lines in ",TRIM(ADJUSTL(args(2)))," = ",NR
 
! defines the number of molecular orbitals and coefficients within a file
DO i=1,NR
  READ(1, '(A)',IOSTAT=ios) line
  IF (line(1:23)=="Alpha Orbital Energies") THEN
    READ(line,FMT=30)title,nmo
    write(*,*) "  number of orbitals = ",nmo
  ENDIF
  IF (line(1:22)=="Alpha MO coefficients") THEN
    READ(line,FMT=30)title,ncoef
    write(*,*) "  number of coefficients = ",ncoef
  ENDIF
ENDDO
REWIND(1)

! defines number of lines required to print coefficients
IF (MOD(ncoef,5)>0) THEN
  nclines=(ncoef/5)+1
ELSE
  nclines=(ncoef/5)
ENDIF
write(*,*) "  number of lines for coefficients = ",nclines

! allocates the size of vecB
ALLOCATE(vecB((ncoef/nmo)*(ncoef/nmo)))

xline(1:len(xline))=REPEAT('X',(16*5))

! grabs coefficient vectors for file B
DO i=1,NR
  READ(1, '(A)',IOSTAT=ios) line
  IF (line(1:22)=="Alpha MO coefficients") then
    DO j=1,nclines
      READ(1, '(A)',IOSTAT=ios) xline
      IF (j<nclines) THEN
        DO k=1,5
          READ(xline(((k-1)*16)+1:k*16),FMT=1) vecB(((j-1)*5)+k)
        ENDDO
      ELSEIF (j==nclines) THEN
        DO k=1,MOD(ncoef,5)
          READ(xline(((k-1)*16)+1:k*16),FMT=1) vecB(((j-1)*5)+k)
        ENDDO
      ENDIF
    ENDDO
  EXIT
  ENDIF
ENDDO
close(1)

! reorganize vecA and vecB into matA & matB
cpermo=ncoef/nmo
write(*,*) "Number of coefficients per orbital = ",cpermo
write(*,*) "Now forming coefficient matrices..."
ALLOCATE(matA(cpermo,cpermo),matB(cpermo,cpermo))
DO i=1,nmo
  matA(i,1:cpermo)=vecA((cpermo*(i-1))+1:(cpermo*i)) ! row vector
  matB(1:cpermo,i)=vecB((cpermo*(i-1))+1:(cpermo*i)) ! column vector
ENDDO

! normalizing all MO vectors
write(*,*) "Normalizing all MO vectors to 1"
ALLOCATE(normA(nmo),normB(nmo))
sumsqA=0.0
sumsqB=0.0
DO i=1,cpermo
  DO j=1,cpermo
    sumsqA=sumsqA+(matA(i,j)*matA(i,j))
    sumsqB=sumsqB+(matB(j,i)*matB(j,i))
  ENDDO
  normA(i)=(1.0/SQRT(sumsqA))
  normB(i)=(1.0/SQRT(sumsqB))
  sumsqA=0.0
  sumsqB=0.0
ENDDO
DO i=1,cpermo
  DO j=1,cpermo
    matA(i,j)=matA(i,j)*normA(i)
    matB(j,i)=matB(j,i)*normB(i)
  ENDDO
ENDDO

!sumsqA=0.0
!DO i=1,cpermo
!  DO j=1,cpermo
!    sumsqA=sumsqA+(matA(i,j)*matA(i,j))
!  ENDDO
!  write(*,*) sumsqA
!  sumsqA=0.0
!ENDDO

! determines the magnitude of each mo-vector
write(*,*) "Determining the magnitude of MO-vectors..."
ALLOCATE(matAT(cpermo,cpermo),matBT(cpermo,cpermo))
ALLOCATE(magA(nmo),magB(nmo))
matAT=matA
matAT=TRANSPOSE(matA)
matBT=matB
matBT=TRANSPOSE(matB)
DO i=1,nmo
  magA(i)=SQRT(DOT_PRODUCT(matA(i,1:cpermo),matAT(1:cpermo,i)))
  magB(i)=SQRT(DOT_PRODUCT(matBT(i,1:cpermo),matB(1:cpermo,i)))
ENDDO

! creates matrix of dot products b/t mo-vectors of a and b
write(*,*) "Determining dot-product of MO-vectors..."
ALLOCATE(dotAB(nmo,nmo))
dotAB=MATMUL(matA,matB)

! creates matrix where each element defined as (a.b/|a||b|)
write(*,*) "Forming matrix where each element defined as (a.b/|a||b|)..."
DO i=1,nmo
  DO j=1,nmo
! handles division by zero
    IF (magA(i)*magB(j).lt.EPS) THEN
      dotAB(i,j)=dotAB(i,j)/(magA(i)*magB(j)+EPS)
    ELSEIF (magA(i)*magB(j).gt.EPS) THEN
      dotAB(i,j)=dotAB(i,j)/(magA(i)*magB(j))
    ENDIF
! Check that all dotAB(i,j) b/t -1 and 1
    IF (dotAB(i,j).gt.(1.0)) THEN
      dotAB(i,j)=1.0
    ELSEIF (dotAB(i,j).lt.(-1.0)) THEN
      dotAB(i,j)=-1.0
    ENDIF
  ENDDO
ENDDO

! creates angle matrix between all MO-vectors
write(*,*) "Forming angle matrix..."
ALLOCATE(angles(nmo,nmo))
DO i=1,nmo
  DO j=1,nmo
    angles(i,j)=(ACOS(dotAB(i,j)))*(180.0/pi)
!    IF (angles(i,j).gt.(90.0)) THEN
!      angles(i,j)=180.0-angles(i,j)
!    ENDIF
  ENDDO
ENDDO

! writes angles to output file
write(*,*) "Writing angle data to angles.dat..."
OPEN(UNIT=3,FILE='angles.dat')
DO i=1,nmo
  DO j=1,nmo
     IF (angles(i,j).lt.(50.0)) THEN
    IF (nargs.eq.4) THEN
      IF (i==mo1 .and. j==mo2) THEN
        write(*,*) " mo1  mo2    angle"
        write(*,FMT=33)i,j,angles(i,j)
      ENDIF
    ENDIF
    write(3,FMT=33)i,j,angles(i,j)
     ENDIF
  ENDDO
ENDDO
close(3)

ENDIF

CALL CPU_TIME(t2)

write(*,*) "CPU_TIME :: ",t2-t1

! Various other assignments
99 continue
30 FORMAT(a50,i12)
1 FORMAT(E16.8)
2 FORMAT(E16.8,E16.8)
3 FORMAT(E16.8,E16.8,E16.8)
4 FORMAT(E16.8,E16.8,E16.8,E16.8)
31 FORMAT(E16.8,E16.8,E16.8,E16.8,E16.8)
33 FORMAT(I5,I5,F10.3)


end program moVecAngle
