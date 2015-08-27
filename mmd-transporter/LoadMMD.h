#pragma once
#include <maya\MPxCommand.h>

/*
* @brief loadmmd�R�}���h
*/
class LoadMMD : public MPxCommand
{
public:
	static const MString cmdName;

	LoadMMD();

	virtual ~LoadMMD();

	static void* creator();

	MStatus doIt(const MArgList& args);
};