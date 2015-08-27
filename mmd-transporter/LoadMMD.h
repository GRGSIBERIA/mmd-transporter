#pragma once
#include <maya\MPxCommand.h>

/*
* @brief loadmmdƒRƒ}ƒ“ƒh
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