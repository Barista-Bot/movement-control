#!/bin/sh -x

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

cd "/home/human/hcr2013/exercises/navigation_tutorial/src/common"

# todo --install-layout=deb per platform
# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
/usr/bin/env \
    PYTHONPATH="/home/human/hcr2013/exercises/navigation_tutorial/install/lib/python2.7/dist-packages:/home/human/hcr2013/exercises/navigation_tutorial/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/human/hcr2013/exercises/navigation_tutorial/build" \
    "/usr/bin/python" \
    "/home/human/hcr2013/exercises/navigation_tutorial/src/common/setup.py" \
    build --build-base "/home/human/hcr2013/exercises/navigation_tutorial/build/common" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/human/hcr2013/exercises/navigation_tutorial/install" --install-scripts="/home/human/hcr2013/exercises/navigation_tutorial/install/bin"
