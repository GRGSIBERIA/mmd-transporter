#include "LoadMMD.h"

const MString LoadMMD::cmdName("loadmmd");

LoadMMD::LoadMMD()
{
}

LoadMMD::~LoadMMD()
{
}

void * LoadMMD::creator()
{
	return new LoadMMD();
}

MStatus LoadMMD::doIt(const MArgList& args)
{
	return MStatus();
}


