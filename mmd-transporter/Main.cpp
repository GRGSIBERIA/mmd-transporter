#include <maya/MFnPlugin.h>

MStatus initializePlugin(MObject obj)
{
	MFnPlugin plugin(obj, "Eiichi Takebuchi(GRGSIBERIA)", "1.0", "Any");
	return MStatus::kSuccess;
}

MStatus uninitializePlugin(MObject obj)
{
	MFnPlugin plugin(obj);
	return MStatus::kSuccess;
}